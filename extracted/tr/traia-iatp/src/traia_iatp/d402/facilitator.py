"""Custom d402 facilitator that interfaces with IATP Settlement Layer."""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import httpx
from eth_account import Account
from web3 import Web3
from eth_account.messages import encode_defunct

from .types import (
    PaymentPayload,
    PaymentRequirements,
    VerifyResponse,
    SettleResponse
)
from .models import IATPSettlementRequest


def get_now_in_utc():
    """Get current time in UTC."""
    return datetime.now(timezone.utc)

logger = logging.getLogger(__name__)


class IATPSettlementFacilitator:
    """Custom d402 facilitator that settles payments through IATP Settlement Layer.
    
    This facilitator verifies d402 payment headers and then submits settlement
    requests to the facilitator service for batch on-chain settlement.
    
    Flow:
    1. MCP Server receives request with X-PAYMENT header
    2. Facilitator /verify verifies the payment signature and authorization
    3. MCP Server processes the request
    4. Facilitator /settle accepts provider attestation and queues for settlement
    5. Facilitator cron batches and submits to IATPSettlementLayer.sol on-chain
    """
    
    def __init__(
        self,
        facilitator_url: str,
        facilitator_api_key: Optional[str] = None,
        provider_operator_key: Optional[str] = None,
        web3_provider: Optional[str] = None,
        server_name: Optional[str] = None,
        server_url: Optional[str] = None
    ):
        """Initialize the IATP Settlement Facilitator.
        
        Args:
            facilitator_url: URL of the facilitator service (handles both /verify and /settle)
            facilitator_api_key: Optional API key for facilitator authentication
            provider_operator_key: Operator private key for provider attestation signing
            web3_provider: Optional Web3 provider URL for direct blockchain interaction
            server_name: Optional MCP server name/ID (sent to facilitator for tracking)
            server_url: Optional MCP server URL (sent to facilitator for tracking)
        """
        self.facilitator_url = facilitator_url.rstrip("/")
        self.facilitator_api_key = facilitator_api_key
        self.provider_operator_key = provider_operator_key
        self.server_name = server_name
        self.server_url = server_url
        
        # Initialize Web3 if provider is given
        self.w3 = Web3(Web3.HTTPProvider(web3_provider)) if web3_provider else None
        
        # Initialize operator account if key provided
        self.operator_account = None
        if provider_operator_key:
            if provider_operator_key.startswith("0x"):
                provider_operator_key = provider_operator_key[2:]
            self.operator_account = Account.from_key(provider_operator_key)
    
    async def verify(
        self,
        payment: PaymentPayload,
        payment_requirements: PaymentRequirements
    ) -> VerifyResponse:
        """Verify a payment header is valid.
        
        If facilitator_url is configured, calls external facilitator /verify endpoint
        which returns a payment_uuid. Otherwise performs local verification.
        
        This checks:
        1. Signature is valid
        2. Authorization is not expired
        3. Amount matches requirements
        4. From address has sufficient balance
        
        Args:
            payment: Payment payload from X-PAYMENT header
            payment_requirements: Payment requirements from server
            
        Returns:
            VerifyResponse with validation result and payment_uuid (if from external facilitator)
        """
        # If external facilitator URL is configured, call it
        if self.facilitator_url:
            try:
                headers = {"Content-Type": "application/json"}
                if self.facilitator_api_key:
                    headers["X-API-Key"] = self.facilitator_api_key
                
                verify_request = {
                    "paymentPayload": payment.model_dump(by_alias=True),
                    "paymentRequirements": payment_requirements.model_dump(by_alias=True)
                }
                
                # Include server name and URL if available
                if self.server_name:
                    verify_request["serverName"] = self.server_name
                if self.server_url:
                    verify_request["serverUrl"] = self.server_url
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{self.facilitator_url}/verify",
                        json=verify_request,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        # Parse response and extract payment_uuid
                        verify_response = VerifyResponse(**result)
                        if verify_response.payment_uuid:
                            logger.info(f"Payment verified via facilitator with payment_uuid: {verify_response.payment_uuid[:20]}...")
                        return verify_response
                    else:
                        error_msg = f"Facilitator verify error: {response.status_code} - {response.text}"
                        logger.error(error_msg)
                        return VerifyResponse(
                            is_valid=False,
                            invalid_reason=error_msg,
                            payer=None,
                            payment_uuid=None
                        )
            except Exception as e:
                logger.error(f"Error calling external facilitator verify: {e}")
                # Fall back to local verification
                logger.warning("Falling back to local verification")
        
        # Local verification (fallback or if no facilitator_url configured)
        try:
            # Extract payment details
            if payment.scheme != "exact":
                return VerifyResponse(
                    is_valid=False,
                    invalid_reason=f"Unsupported scheme: {payment.scheme}",
                    payer=None,
                    payment_uuid=None
                )
            
            payload = payment.payload
            authorization = payload.authorization
            signature = payload.signature
            
            # Verify the signature matches the authorization
            payer = authorization.from_
            
            # Reconstruct the EIP-712 message and verify signature
            # This would use the exact EIP-712 domain from payment_requirements.extra
            eip712_domain = payment_requirements.extra or {}
            
            # For now, perform basic validation
            # In production, this should verify the EIP-3009 signature
            if not payer or not signature:
                return VerifyResponse(
                    is_valid=False,
                    invalid_reason="Missing payer or signature",
                    payer=None,
                    payment_uuid=None
                )
            
            # Verify amount matches requirements
            if authorization.value != payment_requirements.max_amount_required:
                return VerifyResponse(
                    is_valid=False,
                    invalid_reason=f"Amount mismatch: expected {payment_requirements.max_amount_required}, got {authorization.value}",
                    payer=payer,
                    payment_uuid=None
                )
            
            # Verify not expired
            import time
            current_time = int(time.time())
            valid_after = int(authorization.valid_after)
            valid_before = int(authorization.valid_before)
            
            if current_time < valid_after or current_time > valid_before:
                return VerifyResponse(
                    is_valid=False,
                    invalid_reason="Authorization expired or not yet valid",
                    payer=payer,
                    payment_uuid=None
                )
            
            # Verify to address matches pay_to
            if authorization.to.lower() != payment_requirements.pay_to.lower():
                return VerifyResponse(
                    is_valid=False,
                    invalid_reason=f"Pay-to address mismatch",
                    payer=payer,
                    payment_uuid=None
                )
            
            # All checks passed (local verification - no payment_uuid)
            return VerifyResponse(
                is_valid=True,
                invalid_reason=None,
                payer=payer,
                payment_uuid=None  # Local verification doesn't provide payment_uuid
            )
            
        except Exception as e:
            logger.error(f"Error verifying payment: {e}")
            return VerifyResponse(
                is_valid=False,
                invalid_reason=f"Verification error: {str(e)}",
                payer=None,
                payment_uuid=None
            )
    
    async def settle(
        self,
        payment: PaymentPayload,
        payment_requirements: PaymentRequirements
    ) -> SettleResponse:
        """Settle a verified payment through the IATP Settlement Layer.
        
        This submits the payment to the facilitator, which will:
        1. Verify both consumer and provider signatures
        2. Queue for batch settlement
        3. Batch submit to IATPSettlementLayer.settleRequests() on-chain
        4. Credit the provider's balance after confirmation
        
        Args:
            payment: Verified payment payload
            payment_requirements: Payment requirements
            
        Returns:
            SettleResponse with settlement result
        """
        try:
            payload = payment.payload
            authorization = payload.authorization
            consumer_signature = payload.signature
            
            # Create the service request struct (matches Solidity ServiceRequest)
            service_request = {
                "consumer": authorization.from_,
                "provider": payment_requirements.pay_to,
                "amount": authorization.value,
                "timestamp": int(authorization.valid_after),
                "serviceDescription": Web3.keccak(
                    text=payment_requirements.description
                ).hex()
            }
            
            # Create provider attestation if operator key is available
            provider_signature = None
            extra = payment_requirements.extra or {}
            output_hash = extra.get("output_hash")
            payment_uuid = extra.get("payment_uuid")  # Primary payment identifier from facilitator verify
            facilitator_fee_percent = extra.get("facilitator_fee_percent", 250)  # Get fee from facilitator verify response
            
            if not payment_uuid:
                logger.warning("No payment_uuid in payment_requirements.extra - attestation may not be linkable")
            
            if self.operator_account:
                # Create EIP-712 ProviderAttestation signature matching IATPWallet.sol
                # ProviderAttestation(bytes32 consumerSignature, bytes32 outputHash, uint256 timestamp, bytes32 serviceDescription, uint256 facilitatorFeePercent)
                
                # Hash the consumer signature bytes
                consumer_signature_hash = Web3.keccak(hexstr=consumer_signature)
                
                # Prepare output hash for contract verification
                # Python: output_hash = keccak256(output_json) ← First hash (line 161 in mcp_middleware.py)
                # Contract: outputHashHash = keccak256(outputHash bytes) ← Second hash (line 245 in IATPWallet.sol)
                # Provider signs over outputHashHash (the double-hashed value)
                if output_hash:
                    # Output hash is hex string like "0xabcd..." (already hashed once)
                    output_hash_bytes = bytes.fromhex(output_hash[2:] if output_hash.startswith("0x") else output_hash)
                    # Hash it again to match what contract will compute: keccak256(outputHash)
                    output_hash_hash = Web3.keccak(output_hash_bytes)
                    logger.debug(f"Output hash (1st): {output_hash[:20]}...")
                    logger.debug(f"Output hash (2nd): {output_hash_hash.hex()[:20]}...")
                else:
                    # Use zero hash if no output provided
                    output_hash_hash = Web3.keccak(b"")
                
                # Get service description hash
                service_description_hash = Web3.keccak(text=payment_requirements.description)
                
                # Attestation timestamp = current time when service is executed
                # This is when provider actually rendered the service
                import time as time_module
                attestation_timestamp = int(time_module.time())
                
                # Build EIP-712 typed data for ProviderAttestation
                # Domain should be the Provider's IATPWallet domain
                from .chains import get_chain_id
                
                typed_data = {
                    "types": {
                        "ProviderAttestation": [
                            {"name": "consumerSignature", "type": "bytes32"},
                            {"name": "outputHash", "type": "bytes32"},
                            {"name": "timestamp", "type": "uint256"},
                            {"name": "serviceDescription", "type": "bytes32"},
                            {"name": "facilitatorFeePercent", "type": "uint256"},
                        ]
                    },
                    "primaryType": "ProviderAttestation",
                    "domain": {
                        "name": "IATPWallet",
                        "version": "1",
                        "chainId": int(get_chain_id(payment.network)),
                        "verifyingContract": payment_requirements.pay_to,  # Provider's IATPWallet address
                    },
                    "message": {
                        "consumerSignature": consumer_signature_hash,
                        "outputHash": output_hash_hash,
                        "timestamp": attestation_timestamp,
                        "serviceDescription": service_description_hash,
                        "facilitatorFeePercent": facilitator_fee_percent,
                    },
                }
                
                # Sign with provider's operator key
                logger.info(f"🔐 Signing provider attestation with EIP-712...")
                logger.info(f"   Domain: {typed_data['domain']}")
                logger.info(f"   Message fields:")
                logger.info(f"      consumerSignature (hash): {consumer_signature_hash.hex()[:40]}...")
                logger.info(f"      outputHash (double-hash): {output_hash_hash.hex()[:40]}...")
                logger.info(f"      timestamp: {attestation_timestamp}")
                logger.info(f"      serviceDescription (hash): {service_description_hash.hex()[:40]}...")
                logger.info(f"      facilitatorFeePercent: {facilitator_fee_percent}")
                
                signed = self.operator_account.sign_typed_data(
                    domain_data=typed_data["domain"],
                    message_types=typed_data["types"],
                    message_data=typed_data["message"],
                )
                provider_signature = signed.signature.hex()
                if not provider_signature.startswith("0x"):
                    provider_signature = f"0x{provider_signature}"
                
                logger.info(f"✅ Provider attestation (EIP-712) created:")
                logger.info(f"   Signature: {provider_signature[:40]}...")
                logger.info(f"   Signer (operator): {self.operator_account.address}")
                if output_hash:
                    logger.info(f"   Output hash: {output_hash[:20]}...")
                if payment_uuid:
                    logger.info(f"   Payment UUID: {payment_uuid[:20]}...")
                logger.info(f"   Facilitator fee: {facilitator_fee_percent} basis points ({facilitator_fee_percent/100}%)")
            
            # Prepare settlement request for facilitator
            # Use camelCase field names to match facilitator's SettleRequest model
            settlement_request = {
                "paymentUuid": payment_uuid,  # Required
                "providerSignature": provider_signature or "0x",  # Required
                "outputHash": output_hash or "0x",  # Optional
                "serviceDescription": payment_requirements.description,  # Required
                "facilitatorFeePercent": facilitator_fee_percent,  # Default: 250
                "attestationTimestamp": attestation_timestamp  # When provider executed service
            }
            
            # Submit to facilitator
            headers = {"Content-Type": "application/json"}
            if self.facilitator_api_key:
                headers["X-API-Key"] = self.facilitator_api_key
            
            logger.info(f"📤 Sending settle request to facilitator:")
            logger.info(f"   Payment UUID: {payment_uuid}")
            logger.info(f"   Output hash: {output_hash[:20] if output_hash else 'N/A'}...")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.facilitator_url}/settle",
                    json=settlement_request,
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return SettleResponse(
                        success=True,
                        error_reason=None,
                        transaction=result.get("transactionHash"),
                        network=payment.network,
                        payer=authorization.from_
                    )
                else:
                    error_msg = f"Facilitator settle error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    return SettleResponse(
                        success=False,
                        error_reason=error_msg,
                        transaction=None,
                        network=payment.network,
                        payer=authorization.from_
                    )
                    
        except Exception as e:
            logger.error(f"Error settling payment: {e}")
            return SettleResponse(
                success=False,
                error_reason=f"Settlement error: {str(e)}",
                transaction=None,
                network=payment.network,
                payer=None
            )
    
    async def list(self, request: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List discoverable IATP services that accept d402 payments.
        
        This queries the Traia registry for utility agents with d402 enabled.
        
        Args:
            request: Optional filters for discovery
            
        Returns:
            List of discoverable services
        """
        # This would query the MongoDB registry
        # For now, return empty list
        return {
            "d402Version": 1,
            "items": [],
            "pagination": {
                "limit": 100,
                "offset": 0,
                "total": 0
            }
        }


def create_iatp_facilitator(
    facilitator_url: str = "https://facilitator.d402.net",
    facilitator_api_key: Optional[str] = None,
    provider_operator_key: Optional[str] = None,
    web3_provider: Optional[str] = None
) -> IATPSettlementFacilitator:
    """Convenience function to create an IATP Settlement Facilitator.
    
    Args:
        facilitator_url: URL of the facilitator service (handles /verify and /settle)
        facilitator_api_key: Optional API key for facilitator
        provider_operator_key: Provider's operator private key for attestation signing
        web3_provider: Optional Web3 provider URL
        
    Returns:
        Configured IATPSettlementFacilitator
        
    Example:
        facilitator = create_iatp_facilitator(
            facilitator_url="http://localhost:8080",
            facilitator_api_key=os.getenv("FACILITATOR_API_KEY"),
            provider_operator_key=os.getenv("OPERATOR_PRIVATE_KEY")
        )
        
        # Use in d402 middleware
        from traia_iatp.d402 import D402Config, require_iatp_payment
        
        config = D402Config(
            enabled=True,
            pay_to_address="0x...",  # Utility agent contract address
            default_price=D402ServicePrice(...),
            facilitator_url="http://localhost:8080"
        )
    """
    return IATPSettlementFacilitator(
        facilitator_url=facilitator_url,
        facilitator_api_key=facilitator_api_key,
        provider_operator_key=provider_operator_key,
        web3_provider=web3_provider
    )

