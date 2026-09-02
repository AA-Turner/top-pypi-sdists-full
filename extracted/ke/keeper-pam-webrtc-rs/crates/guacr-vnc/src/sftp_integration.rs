// SFTP integration helper for VNC handler
// Reuses code from guacr-sftp handler

#[cfg(feature = "sftp")]
use log::info;
#[cfg(feature = "sftp")]
use russh_sftp::client::SftpSession;

/// Handle Guacamole file instruction for SFTP
///
/// Format:
/// - Upload: file,<stream>,<mimetype>,<filename>,<base64-data>
/// - Download: file,<stream>,<mimetype>,<filename>
#[cfg(feature = "sftp")]
#[allow(dead_code)]
pub async fn handle_sftp_file_request(
    sftp: &mut SftpSession,
    args: &[String],
    to_client: &tokio::sync::mpsc::Sender<bytes::Bytes>,
) -> Result<(), String> {
    use base64::Engine;
    use bytes::Bytes;
    use guacr_protocol::{format_blob, format_end};

    if args.len() < 3 {
        return Err(
            "Invalid file instruction: need at least stream, mimetype, filename".to_string(),
        );
    }

    let stream_id: u32 = args[0]
        .parse()
        .map_err(|_| "Invalid stream ID".to_string())?;
    let _mimetype = &args[1];
    let filename = &args[2];

    // Check if this is upload (has data) or download request
    if args.len() >= 4 {
        // Upload: file,<stream>,<mimetype>,<filename>,<base64-data>
        let data = base64::engine::general_purpose::STANDARD
            .decode(&args[3])
            .map_err(|e| format!("Invalid base64 data: {}", e))?;

        // Write file via SFTP (russh-sftp 2.1 API)
        sftp.write(filename.clone(), &data)
            .await
            .map_err(|e| format!("SFTP write failed: {}", e))?;

        info!("SFTP: File uploaded: {} ({} bytes)", filename, data.len());

        // Send success response
        let response = format_end(stream_id);
        to_client
            .send(Bytes::from(response))
            .await
            .map_err(|e| format!("Failed to send response: {}", e))?;
    } else {
        // Download: file,<stream>,<mimetype>,<filename>
        // Read file via SFTP (russh-sftp 2.1 API)
        let file_data = sftp
            .read(filename.clone())
            .await
            .map_err(|e| format!("SFTP read failed: {}", e))?;

        // Send file data via blob instructions
        let base64_data = base64::engine::general_purpose::STANDARD.encode(&file_data);

        // Send blob instruction
        let blob_instr = format_blob(stream_id, &base64_data);
        to_client
            .send(Bytes::from(blob_instr))
            .await
            .map_err(|e| format!("Failed to send blob: {}", e))?;

        // Send end instruction
        let end_instr = format_end(stream_id);
        to_client
            .send(Bytes::from(end_instr))
            .await
            .map_err(|e| format!("Failed to send end: {}", e))?;

        info!(
            "SFTP: File downloaded: {} ({} bytes)",
            filename,
            file_data.len()
        );
    }

    Ok(())
}
