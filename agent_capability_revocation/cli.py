"""CLI for agent-capability-revocation."""
import sys
import argparse
from .revocation import AgentCapabilityVault


def main():
    parser = argparse.ArgumentParser(description="Agent Capability Revocation")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        vault = AgentCapabilityVault()
        tok = vault.issue_token("deploy_app", max_invocations=2, ttl_seconds=10)
        print(f"Issued token: {tok.token_id}")
        r1 = vault.authorize_and_consume(tok.token_id, "deploy_app")
        print(f"Call 1: {r1}")
        r2 = vault.authorize_and_consume(tok.token_id, "deploy_app")
        print(f"Call 2: {r2}")
        r3 = vault.authorize_and_consume(tok.token_id, "deploy_app")
        print(f"Call 3: {r3}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
