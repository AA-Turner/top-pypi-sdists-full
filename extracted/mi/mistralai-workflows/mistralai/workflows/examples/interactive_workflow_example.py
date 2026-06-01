"""
Example: Interactive Workflow for Expense Approval

Demonstrates InteractiveWorkflow for building workflows that require human input at specific
points. Useful for approval processes, data collection, or multi-step decision making.
"""

import asyncio

from pydantic import BaseModel, Field

import mistralai.workflows as workflows
from mistralai.workflows import InteractiveWorkflow, workflow

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)


class ExpenseRequest(BaseModel):
    employee_id: str
    amount: float
    category: str
    description: str


class ApprovalDecision(BaseModel):
    approved: bool
    reason: str = Field(description="Reason for approval or rejection")
    approved_amount: float | None = Field(
        default=None, description="If different from requested amount (partial approval)"
    )


class ExpenseResult(BaseModel):
    status: str  # approved, rejected, or partial
    final_amount: float
    approval_chain: list[str]
    notes: str


@workflows.workflow.define(name="expense-approval-workflow")
class ExpenseApprovalWorkflow(InteractiveWorkflow):
    @workflows.workflow.entrypoint
    async def entrypoint(self, expense: ExpenseRequest) -> ExpenseResult:
        approval_chain = []
        current_amount = expense.amount

        logger.info("Waiting for manager approval", employee_id=expense.employee_id, amount=expense.amount)

        manager_decision = await self.wait_for_input(
            ApprovalDecision,
            label=f"Manager Approval - ${expense.amount} {expense.category}",
        )

        approval_chain.append(
            f"Manager: {'approved' if manager_decision.approved else 'rejected'} - {manager_decision.reason}"
        )

        if not manager_decision.approved:
            return ExpenseResult(
                status="rejected",
                final_amount=0.0,
                approval_chain=approval_chain,
                notes=f"Rejected at manager level: {manager_decision.reason}",
            )
        if manager_decision.approved_amount is not None:
            current_amount = manager_decision.approved_amount
            logger.info("Manager approved partial amount", original=expense.amount, approved=current_amount)
        if current_amount > 1000:
            logger.info("Expense requires finance approval", amount=current_amount)

            finance_decision = await self.wait_for_input(
                ApprovalDecision,
                label=f"Finance Approval - ${current_amount} {expense.category}",
            )

            approval_chain.append(
                f"Finance: {'approved' if finance_decision.approved else 'rejected'} - {finance_decision.reason}"
            )

            if not finance_decision.approved:
                return ExpenseResult(
                    status="rejected",
                    final_amount=0.0,
                    approval_chain=approval_chain,
                    notes=f"Rejected at finance level: {finance_decision.reason}",
                )

            if finance_decision.approved_amount is not None:
                current_amount = finance_decision.approved_amount
        if current_amount > 10000:
            logger.info("Expense requires executive approval", amount=current_amount)

            executive_decision = await self.wait_for_input(
                ApprovalDecision,
                label=f"Executive Approval - ${current_amount} {expense.category}",
            )

            approval_chain.append(
                f"Executive: {'approved' if executive_decision.approved else 'rejected'} - {executive_decision.reason}"
            )

            if not executive_decision.approved:
                return ExpenseResult(
                    status="rejected",
                    final_amount=0.0,
                    approval_chain=approval_chain,
                    notes=f"Rejected at executive level: {executive_decision.reason}",
                )

            if executive_decision.approved_amount is not None:
                current_amount = executive_decision.approved_amount
        status = "approved" if current_amount == expense.amount else "partial"

        return ExpenseResult(
            status=status,
            final_amount=current_amount,
            approval_chain=approval_chain,
            notes=f"Approved ${current_amount} of ${expense.amount} requested",
        )


@workflows.workflow.define(name="parallel-review-workflow")
class ParallelReviewWorkflow(InteractiveWorkflow):
    class ReviewInput(BaseModel):
        approved: bool
        comments: str
        score: int = Field(ge=1, le=5, description="Review score from 1-5")

    class ReviewResult(BaseModel):
        approved: bool
        reviews: list[str]
        average_score: float

    @workflows.workflow.entrypoint
    async def entrypoint(self, document_id: str, reviewers: list[str]) -> ReviewResult:
        review_tasks = [
            asyncio.create_task(self.wait_for_input(self.ReviewInput, label=f"Review by {reviewer}"))
            for reviewer in reviewers
        ]

        reviews = await asyncio.gather(*review_tasks)
        all_approved = all(review.approved for review in reviews)
        average_score = sum(review.score for review in reviews) / len(reviews) if reviews else 0.0

        review_summaries = [
            f"{reviewers[i]}: {'approved' if reviews[i].approved else 'rejected'} "
            f"(Score: {reviews[i].score}/5) - {reviews[i].comments}"
            for i in range(len(reviews))
        ]

        return self.ReviewResult(
            approved=all_approved,
            reviews=review_summaries,
            average_score=average_score,
        )


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([ExpenseApprovalWorkflow, ParallelReviewWorkflow]))
