use std::{any::Any, sync::Arc};

use async_trait::async_trait;
use azure_core::auth::TokenCredential;
use azure_identity::{
    ClientSecretCredential, DefaultAzureCredentialBuilder, TokenCredentialOptions,
};
use azure_storage::{CloudLocation, prelude::*};
use azure_storage_blobs::{
    blob::operations::GetBlobResponse,
    container::{Container, operations::BlobItem},
    prelude::*,
};
use common_io_config::AzureConfig;
use common_runtime::get_io_pool_num_threads;
use futures::{StreamExt, TryStreamExt, stream::BoxStream};
use snafu::{IntoError, ResultExt, Snafu};

use crate::{
    FileFormat, GetResult, InvalidRangeRequestSnafu,
    object_io::{FileMetadata, FileType, LSResult, ObjectSource},
    range::GetRange,
    stats::IOStatsRef,
    stream_utils::io_stats_on_bytestream,
};

const AZURE_DELIMITER: &str = "/";
const DEFAULT_GLOB_FANOUT_LIMIT: usize = 1024;
const AZURE_STORAGE_RESOURCE: &str = "https://storage.azure.com/.default";
const AZURE_STORE_SUFFIX: &str = ".dfs.core.windows.net";

#[derive(Debug, Snafu)]
enum Error {
    // Input errors.
    #[snafu(display("Unable to parse URL: \"{}\"", path))]
    InvalidUrl {
        path: String,
        source: url::ParseError,
    },
    #[snafu(display("Continuation tokens are not supported: \"{}\"", token))]
    ContinuationToken { token: String },

    // Generic client errors.
    #[snafu(display(
        "Azure Storage Account not set and is required.\n Set either `AzureConfig.storage_account` or the `AZURE_STORAGE_ACCOUNT` environment variable."
    ))]
    StorageAccountNotSet,
    #[snafu(display("Azure client generic error: {}", source))]
    AzureGeneric { source: azure_storage::Error },
    #[snafu(display("Unable to open {}: {}", path, source))]
    UnableToOpenFile {
        path: String,
        source: azure_storage::Error,
    },

    #[snafu(display("Unable to read data from {}: {}", path, source))]
    UnableToReadBytes {
        path: String,
        source: azure_storage::Error,
    },

    #[snafu(display("Unable to read metadata about {}: {}", path, source))]
    RequestFailedForPath {
        path: String,
        source: azure_storage::Error,
    },

    #[snafu(display("Not Found: \"{}\"", path))]
    NotFound { path: String },

    #[snafu(display("Not a File: \"{}\"", path))]
    NotAFile { path: String },

    #[snafu(display("Unable to grab semaphore. {}", source))]
    UnableToGrabSemaphore { source: tokio::sync::AcquireError },
}

struct ParsedAzureUri {
    pub protocol: String,
    pub account_name: Option<String>,
    pub container_and_key: Option<(String, String)>,
}

impl ParsedAzureUri {
    fn new(protocol: impl Into<String>) -> Self {
        Self {
            protocol: protocol.into(),
            account_name: None,
            container_and_key: None,
        }
    }
}

/// Parse an Azure URI into its components.
/// Returns (protocol, (container, key) if exists, storage account if exists).
fn parse_azure_uri(uri: &str) -> super::Result<ParsedAzureUri> {
    let uri = url::Url::parse(uri).with_context(|_| InvalidUrlSnafu { path: uri })?;

    let mut parsed = ParsedAzureUri::new(uri.scheme());

    // "Container" is Azure's name for Bucket.
    //
    // fsspec supports two URI formats; for compatibility, we will support both as well.
    // PROTOCOL://container/path-part/file
    // PROTOCOL://container@account.dfs.core.windows.net/path-part/file
    // See https://github.com/fsspec/adlfs/ for more details
    //
    // It also supports PROTOCOL://account.dfs.core.windows.net/container/path-part/file
    // but it is not documented
    // https://github.com/fsspec/adlfs/blob/5c24b2e886fc8e068a313819ce3db9b7077c27e3/adlfs/spec.py#L364
    if let Some(host) = uri.host_str() {
        if host.ends_with(AZURE_STORE_SUFFIX) {
            match uri.username() {
                "" => {
                    if let Some((container, key)) = uri.path().split_once('/') {
                        parsed.container_and_key = Some((container.into(), key.into()));
                    }
                }
                username => {
                    parsed.container_and_key = Some((username.into(), uri.path().into()));
                }
            }

            let account_name_len = host.len() - AZURE_STORE_SUFFIX.len();
            parsed.account_name = Some(host[..account_name_len].into());
        } else {
            parsed.container_and_key = Some((host.into(), uri.path().into()));
        }
    }

    Ok(parsed)
}

impl From<Error> for super::Error {
    fn from(error: Error) -> Self {
        use Error::{NotAFile, NotFound, UnableToOpenFile, UnableToReadBytes};
        match error {
            UnableToReadBytes { path, source } | UnableToOpenFile { path, source } => {
                match source.as_http_error().map(|v| v.status().into()) {
                    Some(404 | 410) => Self::NotFound {
                        path,
                        source: source.into(),
                    },
                    Some(401) => Self::Unauthorized {
                        store: super::SourceType::AzureBlob,
                        path,
                        source: source.into(),
                    },
                    None | Some(_) => Self::UnableToOpenFile {
                        path,
                        source: source.into(),
                    },
                }
            }
            NotFound { ref path } => Self::NotFound {
                path: path.into(),
                source: error.into(),
            },
            NotAFile { path } => Self::NotAFile { path },
            _ => Self::Generic {
                store: super::SourceType::AzureBlob,
                source: error.into(),
            },
        }
    }
}

pub struct AzureBlobSource {
    blob_client: Arc<BlobServiceClient>,
    connection_pool_sema: Arc<tokio::sync::Semaphore>,
}

impl AzureBlobSource {
    pub async fn get_client(config: &AzureConfig, uri: &str) -> super::Result<Arc<Self>> {
        let parsed_uri = parse_azure_uri(uri)?;

        let storage_account = if let Some(account_name) = parsed_uri.account_name {
            account_name
        } else if let Some(storage_account) = &config.storage_account {
            storage_account.clone()
        } else if let Ok(storage_account) = std::env::var("AZURE_STORAGE_ACCOUNT") {
            storage_account
        } else {
            // TODO(Clark): Allow no storage account + anonymous access + custom endpoint.
            return Err(Error::StorageAccountNotSet.into());
        };

        let access_key = config.access_key.clone().or_else(|| {
            std::env::var("AZURE_STORAGE_KEY")
                .ok()
                .map(std::convert::Into::into)
        });
        let sas_token = config
            .sas_token
            .clone()
            .or_else(|| std::env::var("AZURE_STORAGE_SAS_TOKEN").ok());
        let bearer_token = config
            .bearer_token
            .clone()
            .or_else(|| std::env::var("AZURE_STORAGE_TOKEN").ok());

        let storage_credentials = if config.anonymous {
            StorageCredentials::anonymous()
        } else if let Some(access_key) = access_key {
            StorageCredentials::access_key(&storage_account, access_key.as_string().clone())
        } else if let Some(sas_token) = sas_token {
            StorageCredentials::sas_token(sas_token)
                .map_err(|e| Error::AzureGeneric { source: e })?
        } else if let Some(bearer_token) = bearer_token {
            StorageCredentials::bearer_token(bearer_token)
        } else if let Some(tenant_id) = &config.tenant_id
            && let Some(client_id) = &config.client_id
            && let Some(client_secret) = &config.client_secret
        {
            let options = TokenCredentialOptions::default();

            StorageCredentials::token_credential(Arc::new(ClientSecretCredential::new(
                options.http_client(),
                options
                    .authority_host()
                    .expect("default authority host should be valid"),
                tenant_id.clone(),
                client_id.clone(),
                client_secret.as_string().clone(),
            )))
        } else {
            let default_creds = DefaultAzureCredentialBuilder::new()
                .build()
                .with_context(|_| AzureGenericSnafu {})?;

            if default_creds
                .get_token(std::slice::from_ref(&AZURE_STORAGE_RESOURCE))
                .await
                .is_ok()
            {
                StorageCredentials::token_credential(Arc::new(default_creds))
            } else {
                log::warn!("Azure credentials resolution failed. Defaulting to anonymous mode.");
                StorageCredentials::anonymous()
            }
        };
        let endpoint_url = if let Some(endpoint_url) = &config.endpoint_url {
            Some(endpoint_url.clone())
        } else {
            std::env::var("AZURE_ENDPOINT_URL").ok()
        };
        let blob_client = if let Some(endpoint_url) = endpoint_url {
            ClientBuilder::with_location(
                CloudLocation::Custom {
                    uri: endpoint_url,
                    account: storage_account,
                },
                storage_credentials,
            )
            .blob_service_client()
        } else if config.use_fabric_endpoint {
            ClientBuilder::with_location(
                CloudLocation::Custom {
                    uri: format!("https://{storage_account}.blob.fabric.microsoft.com"),
                    account: storage_account,
                },
                storage_credentials,
            )
            .blob_service_client()
        } else {
            BlobServiceClient::new(storage_account, storage_credentials)
        };

        let connection_pool_sema = Arc::new(tokio::sync::Semaphore::new(
            (config.max_connections_per_io_thread.max(1) as usize)
                * get_io_pool_num_threads().expect("Should be running in tokio pool"),
        ));

        Ok(Self {
            blob_client: blob_client.into(),
            connection_pool_sema,
        }
        .into())
    }

    async fn list_containers_stream(
        &self,
        protocol: &str,
        io_stats: Option<IOStatsRef>,
    ) -> BoxStream<'_, super::Result<FileMetadata>> {
        let protocol = protocol.to_string();

        // Paginated stream of results from Azure API call.
        let responses_stream = self
            .blob_client
            .clone()
            .list_containers()
            .include_metadata(true)
            .into_stream();

        // Flatmap each page of results to a single stream of our standardized FileMetadata.
        responses_stream
            .map(move |response| {
                if let Some(is) = io_stats.clone() {
                    is.mark_list_requests(1);
                }
                (response, protocol.clone())
            })
            .flat_map(move |(response, protocol)| match response {
                Ok(response) => {
                    let containers = response.containers.into_iter().map(move |container| {
                        Ok(self.container_to_file_metadata(protocol.as_str(), &container))
                    });
                    futures::stream::iter(containers).boxed()
                }
                Err(error) => {
                    let error = Err(Error::AzureGeneric { source: error }.into());
                    futures::stream::iter(vec![error]).boxed()
                }
            })
            .boxed()
    }

    async fn list_directory_stream(
        &self,
        protocol: &str,
        container_name: &str,
        prefix: &str,
        posix: bool,
        io_stats: Option<IOStatsRef>,
    ) -> BoxStream<'_, super::Result<FileMetadata>> {
        let container_client = self.blob_client.container_client(container_name);

        // Clone and own some references that we need for the lifetime of the stream.
        let protocol = protocol.to_string();
        let container_name = container_name.to_string();
        let prefix = prefix.to_string();

        // Blob stores expose listing by prefix and delimiter,
        // but this is not the exact same as a unix-like LS behaviour
        // (e.g. /somef is a prefix of /somefile, but you cannot ls /somef)
        // To use prefix listing as LS, we need to ensure the path given is exactly a directory or a file, not a prefix.

        // It turns out Azure list_blobs("path/") will match both a file at "path" and a folder at "path/", which is exactly what we need.
        let prefix_with_delimiter = format!(
            "{}{AZURE_DELIMITER}",
            prefix.trim_end_matches(&AZURE_DELIMITER)
        );
        let full_path = format!("{protocol}://{container_name}{prefix}");
        let full_path_with_trailing_delimiter = format!(
            "{}://{}{}",
            protocol, container_name, &prefix_with_delimiter
        );

        let mut unchecked_results = self
            .list_directory_delimiter_stream(
                &container_client,
                &protocol,
                &container_name,
                &prefix_with_delimiter,
                &posix,
                io_stats.clone(),
            )
            .await;

        // The Azure API call result is almost identical to the desired list directory result
        // with a couple of exceptions:
        // 1. Nonexistent paths return an empty list instead of 404.
        // 2. A file "path" can be returned for a lookup "path/", which is not the desired behaviour.
        //
        // To check for and deal with these cases,
        // manually process the first two items of the stream.

        let mut maybe_first_two_items = vec![];
        let mut stream_exhausted = false;
        for _ in 0..2 {
            let item = unchecked_results.next().await;
            if let Some(item) = item {
                maybe_first_two_items.push(item);
            } else {
                stream_exhausted = true;
                break;
            }
        }

        // Make sure the stream is pollable even if empty,
        // since we will chain it later with the two items we already popped.
        let unchecked_results = if stream_exhausted {
            futures::stream::iter(vec![]).boxed()
        } else {
            unchecked_results
        };

        match &maybe_first_two_items[..] {
            [] => {
                // Check whether the path actually exists.
                let s = async_stream::stream! {
                    let prefix_exists = match prefix.as_str() {
                        "" | "/" => true,
                        _ => {
                            // To check whether the prefix actually exists, check whether it      // Make s::{St{St{Stost ideome ult
      abovndex, r           // To check whet(l resuort Imagety listuesterused fment, tead ult
    defa         });
         refix_existsup.maxdi    ly exis" is/up.ma/blah/         )));
                    ches(&AZURE_DELIMITER)
        );
 s" is/up.ma/blah         )));
                    ches(&AZURE_DELIMI|c:er wr| c

        //    ER)
        );
 ;s" is/up.ma/"
        });
         refix_existsup.max   };

f
            ry_delimiter_stream(
                &container_cl   &container_client,
                &protocol,
     &protocol,
                &container_na   &container_name,
                &prefix_with_________________up.maxdi      &protocol,
     &protocol,
             io_stats.clon   io_stats.clone(),
               io_stats.clon   io_stats.        iex, r           // To check whetA the ex     ensurous mar standarditadata>> {
        ldex, r           // To check whetWe wng iniour
tount p{St{soon{St{ranteof /soan beE_DEL     io_stats.clon   io_stats.//ot a
   anteof /sn,
         io_stats.clon   io_stats.up.max   };

f
             )));
                    crrorok(|(protinfo| (protinfo.(pro!("{pr=th_trailing_delimiter = format!(
 )        )));
                    ct    kip_ing S(|isRE_DEL|eam::iter(am::it::
    (Ok(!isRE_DEL else {
    ));
                    ct   n     se {
    ));
                    c     ?se {
    ));
                    cis_  //  se {
    ));
                 Err(error) =>              futures::strege mode isly exisort Images::{S,s pollable e let streyieldeam of our         
         io_stats.clon   i// O antwi| maumentea    eck tead ult
    yfter repty list instead    let protocol             if ! = match prefi                 // To cheyieldeureGeneric th: String },

  ormat!("{p             Err(error) =>     
rr(error) =>              futures::s            }
        
rr(error) =>[y_fr              // Check whetherIf rep foram of our   };
ensure the pa it      // Mappedskup "path/ult
    yfe}"
     prefix    // Check whetherin the de  //image ibute
pubult
    yfort Imagets, check whett mut maybe        if ormat!("{E_STORE>eady .(pro!("{E_STORE         let error = Err(Error::AzureGeneric th: String },

  ormat!("{p                  futures::stream::iter(vec![error]).boxed()
                }
                       stream_exhausstream::iter(vec![error]).wo_items[..] {
       se {
    ));
            .r wit(ults
        };

 se {
    ));
            .           }
            })
           
 => {
           am::iter(vec![error]).wo_items[..] {
       se {
    ));
    .r wit(ults
        };

 se {
    ));
    .          }
}

pub struct list_directory_stream(
     eam(
                &cont  protocol: &stent,
           : & Azure's toragetocol: &str,
        container_name: &str,
        prefix: &str,
        posix: bool,
       & io_stats: Option<IOStatsRef>,
    ) -> BoxStream<'_, super::Result<FileMetadata>> {
        let containerher allslobs("path/") wil items we 
     containerherter ty liswo iteost ide |(rtekup ter FileMetadata.onent
        respolone and own some references that we need for the lifetime of the stream.
        let protocol = protocol.to_string();
        let container_name = container_name.to_string();
        let prefix = prefix.to_string();

        // Blob stores eeam of res         lable eI call.
      .mut stream_exhauseam = self
        ent,
           .ath/") will).ing();(ing();
         }lob stores eSete neeormat!(
   latetrigger "eam(
    -/ # R the desira
     viour
lfment,    procenesult
     tats: Optif *           stream_exeam = self
        eam = self
     .ormat!(
 (ER)
        );


        //    }

    Okmut stream_exeam = self
        eam = self
     .;

        // Flatmap each Mof results to a single streamts to a FileMetadata.
        responses_stream
            .map(move |response| {
                if let Some(is) = io_stats.clone() {
                    is.mark_list_requests(1);
                }
                (response, protocol.clone())
           ame, &prefix_wit         })
            .flat_map(move |(response, protocol)| match respame, &prefix_witonse {
                Ok(response) => {
                    let containers = an em_: {}"ntainers.in) wil.em);
 ap(move |container| {
ontaiem);               Ok(self.container_to_ontaiem);data(protocol.as_s          ame,
             &ontaiem);          });
                    futures::stream::iter(containers).ban em_: {}             }
                Err(error) => {
                    let error = Err(Error::AzureGeneric ForPath {
        path: String,,,,,,,,,,,,,,,,,},

  oocol}://{                     ame,
             &ing();          account: storrrrr }.into());
          },
                   },
                           futures::stream::iter(vec![error]).boxed()
                }
            })
            .boxed()
    }

    async fn listerieile_metadata(protocol.as_s  prottr,
        contContainer,  & Azure's m<'_,
        rest containerherNB: Cef)
  patwo iroughstregeneric erro's .url()Method,s antecontainerherbecastintheypty listURIam.

a ve yfoif we nthe encod(age_acco.time"part/file
  )ponses_str
        rest containerlistepro!("{:otocol}://{container_nam}not me,
         ))  s.name()
      binb     container_andepro does esult, O::Dlt
        }
}

pub struct listfn ontaiem);data(protocol.as_s    &cont  protocol: &str,
        container_name: &str,
        prefix: &str,ontaiem);: &  preludxStream<'_,
        rest containerfile atntaiem);  BlobServiceClientelud    pr(tnta     
        rest containerlistlistepro!("{:otocol}://{container_nam}n     e,
             &onta   ))  s.name()
          binboken) nta paftResdefayo3 = {;
  gth  s.name()
        epro does esult, O::oRead})
           ,BlobServiceClientelud    prPng();(ing();     
        rest containerlistlistepro!("{:otocol}://{container_nam}n     e,
             &ing();
  ))  s.name()
          binb     container_and_andepro does esult, O::Dlt
        }
}

pu     ,BlobServib struct listprotInt, urlnum_tconstfor tort INOT a,
}

s      , source) listprotUzureby `get()` the ded.
     holdira
 ermit (avoidsese dloal with stats::::Suf(); ) listclient(config
     nt, urls    &cont  protocol: &st super::Rstats: Option<IOStatsRef>,
    ) -> BoxStream<'_,<FileMetadata>     et parsed_uri = parse_azure_uri(uri)?;

        let arsed_uri = ey) if exists, staccount_name.boxed()
    }_key = Some((host.boxed()
    }ok_d::env::vareneric         path: String,,,,,,,,,;

    le            source: error.into(),or,
    },
    ::EteadHos      &protocol     if defaulif;
    s_stead            is.maror::StorageAccounth: String },

   le       p                  fOkmut stream_exent = self.blob_client.container_client(container_name);

    ) blob_client = if let Some(eent,
           . if let Som(s, s mut stream_exh    rest== if let Som.boxed()
    }nfigpaftResdef  .include_metad         .is_ok()
ayo3 =xt(ile {
               ::Self {
 ng },

   le       p let arsed_urs) = io_stats.clone() {
   asTORAG           is.marequestshead
                }
   Okmut streaOk_siz  resp nta paftResdefayo3 = {;
  gth              *ct Az#[use azure_c]obSour,
    range: withce {
    pub async fn client(coOCOL://a_ge,
 s  prott_per::Result<Arc<Self>> {
 io_et parsed_urOk      .intoct list_directorget(    &cont  protocol: &st super::Rstats: Optge,
  tsRef>,
 stats::oxStrea Option<IOStatsRef>,
    ) -> BoxStream<'_,<FileMetadata>validRanget parsed_uri = permit       .list_directorol_sema,
        }
 .clone()
            .list_containea,
}

s_own        }
       d         .is_ok()
ayo3 =xt(ile {
   { source: toError et storage_accouparse_azure_uri(uri)?;

        let arsed_uri = ey) if exists, staccount_name.boxed()
    }_key = Some((host.boxed()
    }ok_d::env::vareneric         path: String,,,,,,,,,;

    le            source: error.into(),or,
    },
    ::EteadHos      &protocol     if defaulif;
    s_stead            is.maror::StorageAccounth: String },

   le       p                  fOkmut stream_exent = self.blob_client.container_client(container_name);

    ) blob_client = if let Some(eent,
           . if let Som(s, s mut stream_exea     _     
    ontainer_cliget() mut stream_exea     _     
    s) = io_statge,
 clonge,
           is.mare,
 .     at| {
yo3 =xt(equestSnafu,
    object_   Ok(array.attre {
   e,
           is.maaaaa stats::::BStried(u     ea     _     
 .ge,
 su      source: errorherNote: s) a dirgre two thanoan be, segmgeneri lateror::St    wholime:3 = {.        is.maaaaa stats::::Offset(n     ea     _     
 .ge,
 sn..      source: error stats::::Suf();(n     h: String,,,,,,,,,,,,,rotUzuonfig
     nt, urlstreavoidese dloal (pped.
     holdra
 ermit         });
         _streonst Aent.cnfig
     nt, urlsuri,ne() {
                   Ok(array.attr   is.mara     _     
 .ge,
 s
   .s= ["ae ne_sub(n)..     }
            })
           
 => {
              stream_exra     _     
 
 => {
    blob_client = if l
        ea     _     
 .;

        // Flatmap ea Tokewn         .split_        let prefix = pref
         if l
         }
       d nd_then(_direcer| {
v: se,
    containinto respcolle ru        .map(|arr| arr.inr::Azer| {
        if let Some(iytes { path, sour     ::Self {
 ngOk(array.attr   is.ma},

  ewn                      client_secret         },
      .;

  v| v.s      * get_io_pool           &protocol  t arsed_urs) = io_stats.clone() {
   asTORAG           is.marequestsnfig                }
   Ok   }
   Ok(validRang::S          &containeytestream,
};

const AaType:pi:frost A),ne() {
        client_se     container_and_stat ermit      client_se     container async fn list_containeput(    &cont  protocol: &st_ super::Rstats: Opt_: {}: ;

co:: sourstats: Opt_ion<IOStatsRef>,
    ) -> BoxStream<'_,<FileMetadata>() ngOk(array.todo!("PUT stregeneribpose listorted: \"ye\"{}\"", to! Ple //i" and a disu         Sct list_directorgetg
   s  prott super::Rstion<IOStatsRef>,
    ) -> Bom<'_,<FileMetadata>     et parsed_uri = _permit       .list_directorol_sema,
        }
 .clone()
     a,
}

s      }
       d         .is_ok()
ayo3 =xt(ile {
   { source: toError et is_ok()
ent.cnfig
     nt, urlsuri,ne() {
             Sct list_directorg pr( is_ok()
ent.sync::    lstats: Optg prt!("{per::Rstats: Optfanout_mat!(atsRef>,
     etocol: &strls)
  binbsRef>,
i32etocol: &stmat!(atsRef>,
     etocol: &stion<IOStatsRef>,
    ) -> BoxStrea Opt_(prottocol}atsRef>,
etResult, oxStream<'_,<FileMetadata> super::Res<IOSiclt<FileMetadata>> {
        leet parsed_ur    FileForileMeta list_g pr::g pr Flatmap each Eh givefanout_mat!(esired b) =>  \"{r,
  tokioawa
pyo3procencyfull_path_withanout_mat!(e=thanout_mat!(.or=> Ok(FANOUT_LIMIT: usize = 102   }lob storeg pr( is_ok()
k()
ent.     client_seg prt!("{ container_andeanout_mat!( protocol, contls)
  bi.or=> Ok(1000       vec![*h amat!( protocol, conion<IOSt container container          Sct list_director     dir(    &cont  protocol: &st super::Rstats: Opt        io_stats: Opt_rls)
  binbsRef>,
i32etocol: &stion<IOStatsRef>,
    ) -> BoxStream<'_,<FileMetadata> super::Re<FileMetadata>> {
        leet parsed_uri = parse_azure_uri(uri)?;

        let storage_aas_str(ount_name _key = Some((host. // TODO(Clark): Lf 40to_iter().m    client_se    pe::Ten    .list_directoiner rs_stream(
        &sel(ount_name tr(), &container))
e() {
   .list_directoiner       ,// TODO(Clark): Lf 40amtsth itemo a te,
       container_and_statme);

        /.path().s::Ten    .list_directoiner rs_steam(
        &self,
                  (ount_name tr(), &container))f,
                  e, &prefix_wit ntainer))f,
                  ().clone()r))f,
                            io_stats.clon   iion<IOSt containerrrrrrrrr .list_directoiner       ,// TODO(Cb struct list_directoryss    &cont  protocol: &str("{per::Rstats: Opt        io_stats: Optcken { tokenlice::atsRef>,
r::R>stats: Opt_rls)
  binbsRef>,
i32etocol: &stion<IOStatsRef>,
    ) -> BoxStream<'_,<FileMetadata>ectSourcet containerherIt/", wsniour
thge_blob "aut library    containerherort Imageproceney orge acu of ,    pokens are not sup1. Nonexistenage_accodocs.rs/_blobs::{
    blob:/0.15.0/_blobs::{
    blob:/e"part/fillobItem},
/ath/") wil/lobSou.Lf 4
   s_locati.html. Nonexistenage_accodocs.rs/_blobs::{
    blob:/0.15.0/_blobs::{
    blob:/t()
   llobItem},
/lobSou.Lf 4 Azure's s_locati.html. Nonexistenage_accodocs.rs/_blobsnet//0.15.0/_blobsnet//lobSou.Page]
   html. Nonexisas_strcken { tokenlice::. // TODO(Clark    pe::Ten(       vec![*h ad) = &r_token>torageAccounoken { token: Strin.list_directoinerice::atice::_        let     &protocol  ,// TODO(Cbet storage_accoused fm      .list_director     dir(} => {      e     
e() {
   .list_directoc     ?se {
    ));
ct   colle r::<Vec<_>>      }
       d     et storage_aOk(ectSourct containerlisteprot containerrrrrcken { tokenlice::at     container_andnot_fStri_if_stead:res = [// TODO(Cbasync fn listerias_any_arc(ent.sync::    lm<'_,nc::dyn Any + S tes+ Syncet container