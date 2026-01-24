let webCrypto = window.crypto.subtle;

function str_to_array(str){
    let sp = str.split("");
    let rep = new Uint8Array(sp.length);
    for (let i in sp) {
        reply[i] = String.charCodeAt(sp[i]);
    }
    return reply;
}

function url_atob(str) {
    return str_to_array(atob(str.replace(/\-/g, "+").replace(/\_/g, "/")))
}

function main() {
    let private_key = {
        "crv":"P-256",
        "d":"xlC2uc3PnHz9aMMxA-0MjE4nXSFfwhDYAaCphEgDRX8",
        "ext":true,
        "key_ops":["sign"],
        "kty":"EC",
        "x":"azt9CPpJXmL1uLO0FZdqbT7iMKpo-HK-C4r2VIPjTbg",
        "y":"B8K9zYQtAEzTSRl2SXw0gfDa_4rN6i0CLslJfg3TSTc"
    };

    let public_key = {
        "crv":"P-256",
        "ext":true,
        "key_ops":["verify"],
        "kty":"EC",
        "x":"azt9CPpJXmL1uLO0FZdqbT7iMKpo-HK-C4r2VIPjTbg",
        "y":"B8K9zYQtAEzTSRl2SXw0gfDa_4rN6i0CLslJfg3TSTc"
    };


    let alg={name:"ECDSA", namedCurve:"P-256", hash:{name:"SHA-256"}};
    let token = "banana fondue";
    let token_arr = str_to_array(token);
    let signature = "MDEwDQYJYIZIAWUDBAICBQAEMLmwsWj3slLNEyNrrozkvBXBUv-DnDrabDW87y0TOJccZ0qUJBFDTL0impo__4vgBy6JWDLZ_S8OOKRBYh-P5wE=";
    let sig = url_atob(signature);

    webCrypto.importKey('jwk', private_key, "ECDSA", true, ["sign"])
        .then(key=>{
            webCrypto.sign(
                alg,
                key,
                url_atob(token))
                .then(k => console.debug("signature:", k))
                .catch(err => console.error(err))
        })
        .catch(err => console.error(err));

    webCrypto.importKey('jwk', public_key, "ECDSA", true, ["verify"])
        .then(key=>{
            webCrypto.verify(
                    alg,
                    key,
                    url_atob(signature),
                    token_arr)
                .then(k => console.debug(k))
                .catch(err => console.error(err))
        })
        .catch(err=> console.error(err));
}
