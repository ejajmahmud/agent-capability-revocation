"""Core Agent Capability Revocation implementation."""
import time
import secrets
from typing import Dict, Any, Optional


class CapabilityToken:
    def __init__(self, token_id: str, tool_name: str, max_invocations: int, ttl_seconds: float):
        self.token_id = token_id
        self.tool_name = tool_name
        self.max_invocations = max_invocations
        self.invocations_used = 0
        self.created_at = time.time()
        self.expires_at = self.created_at + ttl_seconds
        self.is_revoked = False

    def is_valid(self, requested_tool: str) -> Tuple_Result:
        if self.is_revoked:
            return False, "Token has been explicitly revoked"
        if time.time() > self.expires_at:
            return False, "Token TTL expired"
        if self.invocations_used >= self.max_invocations:
            return False, "Max invocations exhausted"
        if requested_tool != self.tool_name:
            return False, f"Unauthorized tool scope: requested {requested_tool}, authorized for {self.tool_name}"
        return True, "Valid"


Tuple_Result = tuple[bool, str]


class AgentCapabilityVault:
    def __init__(self):
        self._tokens: Dict[str, CapabilityToken] = {}

    def issue_token(self, tool_name: str, max_invocations: int = 5, ttl_seconds: float = 60.0) -> CapabilityToken:
        tid = "CAP_" + secrets.token_hex(6).upper()
        token = CapabilityToken(tid, tool_name, max_invocations, ttl_seconds)
        self._tokens[tid] = token
        return token

    def authorize_and_consume(self, token_id: str, tool_name: str) -> Dict[str, Any]:
        token = self._tokens.get(token_id)
        if not token:
            return {"authorized": False, "reason": "Token not found"}

        valid, reason = token.is_valid(tool_name)
        if not valid:
            return {"authorized": False, "reason": reason}

        token.invocations_used += 1
        return {
            "authorized": True,
            "invocations_used": token.invocations_used,
            "remaining": token.max_invocations - token.invocations_used
        }

    def revoke(self, token_id: str):
        if token_id in self._tokens:
            self._tokens[token_id].is_revoked = True
