"""Tests for agent-capability-revocation."""
import unittest
from agent_capability_revocation.revocation import AgentCapabilityVault


class TestCapabilityRevocation(unittest.TestCase):
    def setUp(self):
        self.vault = AgentCapabilityVault()

    def test_invocations_limit(self):
        tok = self.vault.issue_token("read_db", max_invocations=1)
        r1 = self.vault.authorize_and_consume(tok.token_id, "read_db")
        self.assertTrue(r1["authorized"])
        r2 = self.vault.authorize_and_consume(tok.token_id, "read_db")
        self.assertFalse(r2["authorized"])
        self.assertIn("exhausted", r2["reason"])

    def test_explicit_revocation(self):
        tok = self.vault.issue_token("write_db", max_invocations=10)
        self.vault.revoke(tok.token_id)
        res = self.vault.authorize_and_consume(tok.token_id, "write_db")
        self.assertFalse(res["authorized"])
        self.assertIn("explicitly revoked", res["reason"])
