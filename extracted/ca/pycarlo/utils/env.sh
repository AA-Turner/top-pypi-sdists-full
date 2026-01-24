#!/usr/bin/env bash
set -e

BASEDIR=$(dirname "$0")

# shellcheck disable=SC1091
. "$BASEDIR/.env"

if [ -z "${MCD_API_ENDPOINT}" ]; then
    echo -e '\033[0;31m❌ Error: Missing expected .env variable "MCD_API_ENDPOINT".\033[0m' && exit 1
fi

if [ -z "${MCD_DEFAULT_API_ID}" ] || [ "${MCD_DEFAULT_API_ID}" = "change-me" ]; then
    echo -e '\033[0;31m❌ Error: Missing or invalid .env variable "MCD_DEFAULT_API_ID".\033[0m'
    echo 'Please update utils/.env with your actual API credentials.' && exit 1
fi

if [ -z "${MCD_DEFAULT_API_TOKEN}" ] || [ "${MCD_DEFAULT_API_TOKEN}" = "change-me" ]; then
    echo -e '\033[0;31m❌ Error: Missing or invalid .env variable "MCD_DEFAULT_API_TOKEN".\033[0m'
    echo 'Please update utils/.env with your actual API credentials.' && exit 1
fi

MCD_API_ENDPOINT="${MCD_API_ENDPOINT}" MCD_DEFAULT_API_ID="${MCD_DEFAULT_API_ID}" MCD_DEFAULT_API_TOKEN="${MCD_DEFAULT_API_TOKEN}" exec "$@"
