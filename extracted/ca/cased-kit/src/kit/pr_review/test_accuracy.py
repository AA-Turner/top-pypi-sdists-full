"""Accuracy testing tool for PR reviews."""

import argparse
from typing import Any, Dict, List, cast

from .agentic_reviewer import AgenticPRReviewer
from .config import ReviewConfig
from .reviewer import PRReviewer
from .validator import validate_review_quality


class AccuracyTester:
    """Test and validate PR review accuracy."""

    def __init__(self, config: ReviewConfig):
        self.config = config
        self.standard_reviewer = PRReviewer(config)
        self.agentic_reviewer = AgenticPRReviewer(config)

    def test_pr_across_modes(self, pr_url: str) -> Dict[str, Any]:
        """Test a PR across standard and agentic review modes and compare quality."""
        print(f"🧪 Testing PR: {pr_url}")
        print("=" * 60)

        results = {}

        # Test Standard Mode
        print("\n🛠️  STANDARD MODE")
        print("-" * 20)
        try:
            standard_review = self.standard_reviewer.review_pr(pr_url)
            results["standard"] = {
                "review": standard_review,
                "success": True,
                "cost": self.standard_reviewer.cost_tracker.get_total_cost(),
            }
        except Exception as e:
            print(f"❌ Standard mode failed: {e}")
            results["standard"] = {"success": False, "error": str(e)}

        # Test Agentic Mode (Budget)
        print("\n🤖 AGENTIC MODE (8 turns)")
        print("-" * 20)
        try:
            # Set budget turns
            self.agentic_reviewer.max_turns = 8
            agentic_review = self.agentic_reviewer.review_pr_agentic(pr_url)
            results["agentic"] = {
                "review": agentic_review,
                "success": True,
                "cost": self.agentic_reviewer.cost_tracker.get_total_cost(),
            }
        except Exception as e:
            print(f"❌ Agentic mode failed: {e}")
            results["agentic"] = {"success": False, "error": str(e)}

        # Compare results
        print("\n📊 COMPARISON SUMMARY")
        print("=" * 40)

        for mode, result in results.items():
            if result.get("success"):
                cost = result.get("cost", 0)
                review = cast(str, result.get("review", ""))
                review_length = len(review)
                print(f"{mode.upper():>10}: ${cost:.3f} | {review_length:,} chars")
            else:
                print(f"{mode.upper():>10}: FAILED - {result.get('error', 'Unknown error')}")

        return results

    def validate_existing_review(self, pr_url: str, review_content: str) -> Dict[str, Any]:
        """Validate an existing review against the PR."""
        print(f"🔍 Validating existing review for: {pr_url}")

        try:
            # Get PR data
            owner, repo, pr_number = self.standard_reviewer.parse_pr_url(pr_url)
            files = self.standard_reviewer.get_pr_files(owner, repo, pr_number)
            pr_diff = self.standard_reviewer.get_pr_diff(owner, repo, pr_number)

            # Validate
            changed_files = [f["filename"] for f in files]
            validation = validate_review_quality(review_content, pr_diff, changed_files)

            print(f"📊 Quality Score: {validation.score:.2f}/1.0")
            print(f"📈 Metrics: {validation.metrics}")

            if validation.issues:
                print("⚠️  Issues Found:")
                for issue in validation.issues:
                    print(f"  - {issue}")
            else:
                print("✅ No quality issues detected")

            return {
                "score": validation.score,
                "issues": validation.issues,
                "metrics": validation.metrics,
                "pr_details": {
                    "files": len(files),
                    "additions": sum(f["additions"] for f in files),
                    "deletions": sum(f["deletions"] for f in files),
                },
            }

        except Exception as e:
            print(f"❌ Validation failed: {e}")
            return {"error": str(e)}

    def regression_test(self, pr_urls: List[str]) -> Dict[str, Any]:
        """Run regression tests on multiple PRs."""
        print(f"🧪 Running regression test on {len(pr_urls)} PRs")
        print("=" * 60)

        results = []
        total_cost = 0.0

        for i, pr_url in enumerate(pr_urls, 1):
            print(f"\n[{i}/{len(pr_urls)}] Testing: {pr_url}")
            print("-" * 40)

            try:
                # Test with standard mode
                review = self.standard_reviewer.review_pr(pr_url)
                cost = self.standard_reviewer.cost_tracker.get_total_cost()
                total_cost += cost

                # Get validation data
                owner, repo, pr_number = self.standard_reviewer.parse_pr_url(pr_url)
                files = self.standard_reviewer.get_pr_files(owner, repo, pr_number)
                pr_diff = self.standard_reviewer.get_pr_diff(owner, repo, pr_number)
                changed_files = [f["filename"] for f in files]
                validation = validate_review_quality(review, pr_diff, changed_files)

                result = {
                    "pr_url": pr_url,
                    "success": True,
                    "cost": cost,
                    "quality_score": validation.score,
                    "issues": validation.issues,
                    "metrics": validation.metrics,
                    "pr_size": len(files),
                }

                print(f"✅ Success | Score: {validation.score:.2f} | Cost: ${cost:.3f}")

            except Exception as e:
                result = {"pr_url": pr_url, "success": False, "error": str(e)}
                print(f"❌ Failed: {e}")

            results.append(result)

        # Summary
        successful = [r for r in results if r.get("success") is True]
        avg_score = sum(cast(float, r["quality_score"]) for r in successful) / len(successful) if successful else 0
        avg_cost = sum(cast(float, r["cost"]) for r in successful) / len(successful) if successful else 0

        print("\n📊 REGRESSION TEST SUMMARY")
        print("=" * 40)
        print(f"Total PRs: {len(pr_urls)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(pr_urls) - len(successful)}")
        print(f"Average Quality Score: {avg_score:.2f}/1.0")
        print(f"Average Cost: ${avg_cost:.3f}")
        print(f"Total Cost: ${total_cost:.3f}")

        return {
            "total_prs": len(pr_urls),
            "successful": len(successful),
            "failed": len(pr_urls) - len(successful),
            "avg_quality_score": avg_score,
            "avg_cost": avg_cost,
            "total_cost": total_cost,
            "results": results,
        }


def main():
    """CLI for accuracy testing."""
    parser = argparse.ArgumentParser(description="Test PR review accuracy")
    parser.add_argument("command", choices=["test", "validate", "regression"])
    parser.add_argument("--pr-url", help="PR URL to test")
    parser.add_argument("--review-file", help="File containing review to validate")
    parser.add_argument("--pr-list", help="File containing list of PR URLs for regression testing")
    parser.add_argument("--config", help="Config file path")

    args = parser.parse_args()

    # Load config
    config = ReviewConfig.from_file(args.config) if args.config else ReviewConfig.from_default()
    tester = AccuracyTester(config)

    if args.command == "test":
        if not args.pr_url:
            print("❌ --pr-url required for test command")
            return
        tester.test_pr_across_modes(args.pr_url)

    elif args.command == "validate":
        if not args.pr_url or not args.review_file:
            print("❌ --pr-url and --review-file required for validate command")
            return

        with open(args.review_file, "r") as f:
            review_content = f.read()

        tester.validate_existing_review(args.pr_url, review_content)

    elif args.command == "regression":
        if not args.pr_list:
            print("❌ --pr-list required for regression command")
            return

        with open(args.pr_list, "r") as f:
            pr_urls = [line.strip() for line in f if line.strip()]

        tester.regression_test(pr_urls)


if __name__ == "__main__":
    main()
