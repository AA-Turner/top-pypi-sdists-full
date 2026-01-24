# Check inputs
if [ $# -eq 0 ]
  then
    echo "Script expects 1 argument, wallet prefix, which must have an associated <prefix>.seed file"
    exit -1
fi

prefix=$1
echo "Generating keys for wallet with prefix $prefix..."

# Check if seed file exists
if [ -e $prefix.seed ]
then
    cardano-address key from-recovery-phrase Shelley < ${prefix}.seed > ${prefix}_root.xsk

    # Generate keys for address 0
    cat ${prefix}_root.xsk | cardano-address key child 1852H/1815H/0H/0/0 > ${prefix}_addr0.prv
    cardano-cli key convert-cardano-address-key --shelley-payment-key --signing-key-file ${prefix}_addr0.prv --out-file ${prefix}_addr0.skey
    cardano-cli key verification-key --signing-key-file ${prefix}_addr0.skey --verification-key-file ${prefix}_ext_addr0.vkey
    cardano-cli key non-extended-key --extended-verification-key-file ${prefix}_ext_addr0.vkey --verification-key-file ${prefix}_addr0.vkey

    # Generate stake keys
    cat ${prefix}_root.xsk | cardano-address key child 1852H/1815H/0H/2/0 > ${prefix}_stake.prv
    cardano-cli key convert-cardano-address-key --signing-key-file ${prefix}_stake.prv --shelley-stake-key --out-file ${prefix}_stake.skey
    cardano-cli key verification-key --signing-key-file ${prefix}_stake.skey --verification-key-file ${prefix}_ext_stake.vkey
    cardano-cli key non-extended-key --extended-verification-key-file ${prefix}_ext_stake.vkey --verification-key-file ${prefix}_stake.vkey

    # Generate address
    cardano-cli address build --payment-verification-key-file ${prefix}_addr0.vkey --stake-verification-key-file ${prefix}_stake.vkey --out-file ${prefix}_addr0.addr --testnet-magic 1

    echo "Address: `cat ${prefix}_addr0.addr`"
    echo "VKEY: `cat ${prefix}_addr0.vkey`"
    echo "SKEY: `cat ${prefix}_addr0.skey`"
else
    echo "File containing seed phrase does not exist: $prefix.seed"
fi
