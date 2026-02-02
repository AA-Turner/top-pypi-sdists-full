"""
DSLighting 内置 Operators 使用示例

展示所有内置 Operators 的实际用法
"""

import asyncio
from typing import Dict, Any


# ============================================================================
# 示例 1: ExecuteAndTestOperator - 执行代码
# ============================================================================

async def example_execute_and_test():
    """代码执行 Operator 示例"""
    from dslighting.operators import ExecuteAndTestOperator
    from dslighting.services import SandboxService

    print("=" * 80)
    print("示例 1: ExecuteAndTestOperator")
    print("=" * 80)

    # 创建 sandbox 和 operator
    sandbox = SandboxService()
    op = ExecuteAndTestOperator(sandbox_service=sandbox)

    # Script 模式
    print("\n1. Script 模式:")
    result = await op(code="""
import pandas as pd
import numpy as np

# 创建示例数据
data = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50]
})

print("数据形状:", data.shape)
print("前3行:")
print(data.head(3))
""")

    print(f"成功: {result.success}")
    print(f"输出:\n{result.stdout}")

    if result.stderr:
        print(f"错误:\n{result.stderr}")


# ============================================================================
# 示例 2: PlanOperator - 生成计划
# ============================================================================

async def example_plan():
    """计划生成 Operator 示例"""
    from dslighting.operators import PlanOperator
    from dsat.services.llm import LLMService

    print("\n" + "=" * 80)
    print("示例 2: PlanOperator")
    print("=" * 80)

    # 初始化 LLM
    llm = LLMService()

    # 创建 operator
    op = PlanOperator(llm_service=llm)

    # 生成计划
    plan = await op(user_request="""
分析 bike sharing demand 数据集：
1. 加载数据
2. 探索性数据分析
3. 特征工程
4. 训练模型
5. 评估性能
""")

    print(f"\n生成的计划包含 {len(plan.tasks)} 个任务:")
    for i, task in enumerate(plan.tasks, 1):
        print(f"\n任务 {i} (ID: {task.task_id}):")
        print(f"  描述: {task.instruction}")
        if task.dependent_task_ids:
            print(f"  依赖: {task.dependent_task_ids}")


# ============================================================================
# 示例 3: GenerateCodeAndPlanOperator - 生成代码和计划
# ============================================================================

async def example_generate_code_and_plan():
    """代码和计划生成 Operator 示例"""
    from dslighting.operators import GenerateCodeAndPlanOperator
    from dsat.services.llm import LLMService

    print("\n" + "=" * 80)
    print("示例 3: GenerateCodeAndPlanOperator")
    print("=" * 80)

    # 初始化
    llm = LLMService()
    op = GenerateCodeAndPlanOperator(llm_service=llm)

    # 生成
    plan, code = await op(
        system_prompt="You are a data scientist specializing in exploratory data analysis",
        user_prompt="Load bike.csv and show basic statistics: shape, dtypes, missing values, and summary"
    )

    print("\n生成的计划:")
    print(plan)
    print("\n生成的代码:")
    print(code)


# ============================================================================
# 示例 4: ReviewOperator - 审查结果
# ============================================================================

async def example_review():
    """结果审查 Operator 示例"""
    from dslighting.operators import ReviewOperator
    from dsat.services.llm import LLMService

    print("\n" + "=" * 80)
    print("示例 4: ReviewOperator")
    print("=" * 80)

    # 初始化
    llm = LLMService()
    op = ReviewOperator(llm_service=llm)

    # 审查结果
    review = await op(prompt_context={
        "task": "Train a model to predict bike demand",
        "code": """
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

X = df[features]
y = df['count']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
""",
        "output": """
Model trained successfully.
Training R² score: 0.95
Test R² score: 0.87
"""
    })

    print(f"\n审查结果:")
    print(f"通过: {review.passed}")
    print(f"分数: {review.score:.2f}")
    print(f"理由:\n{review.reasoning}")


# ============================================================================
# 示例 5: SummarizeOperator - 总结内容
# ============================================================================

async def example_summarize():
    """内容总结 Operator 示例"""
    from dslighting.operators import SummarizeOperator
    from dsat.services.llm import LLMService

    print("\n" + "=" * 80)
    print("示例 5: SummarizeOperator")
    print("=" * 80)

    # 初始化
    llm = LLMService()
    op = SummarizeOperator(llm_service=llm)

    # 长篇内容
    long_content = """
实验日志：
1. 第一轮：使用 XGBoost，默认参数
   - 训练时间：120秒
   - 验证分数：0.8234
   - 问题：过拟合明显

2. 第二轮：使用 LightGBM，调整学习率
   - 训练时间：85秒
   - 验证分数：0.8567
   - 改进：使用早停，减少过拟合

3. 第三轮：使用 LightGBM，增加特征工程
   - 添加时间特征：hour, day_of_week, month
   - 添加天气特征交互
   - 训练时间：150秒
   - 验证分数：0.8912

4. 第四轮：集成模型
   - LightGBM + XGBoost stacking
   - 训练时间：300秒
   - 验证分数：0.9045

结论：集成模型效果最好，但训练时间较长。考虑到性能和效率的平衡，
推荐使用第三轮的 LightGBM 模型（带特征工程）作为最终模型。
"""

    # 生成总结
    summary = await op(context=long_content)

    print(f"\n原始内容长度: {len(long_content)} 字符")
    print(f"\n总结后的内容:\n{summary}")


# ============================================================================
# 示例 6: Pipeline - 顺序执行
# ============================================================================

async def example_pipeline():
    """Pipeline 编排示例"""
    from dslighting.operators.orchestration import Pipeline
    from dslighting.operators import (
        GenerateCodeAndPlanOperator,
        ExecuteAndTestOperator
    )
    from dsat.services.llm import LLMService
    from dslighting.services import SandboxService

    print("\n" + "=" * 80)
    print("示例 6: Pipeline - 顺序执行")
    print("=" * 80)

    # 初始化服务
    llm = LLMService()
    sandbox = SandboxService()

    # 创建 Pipeline
    pipeline = Pipeline([
        # Step 1: 生成 EDA 代码
        GenerateCodeAndPlanOperator(llm),

        # Step 2: 执行代码
        ExecuteAndTestOperator(sandbox)
    ])

    # 执行
    result = await pipeline.execute(
        system_prompt="You are a data scientist",
        user_prompt="Generate code to analyze bike.csv: show shape, dtypes, and summary statistics"
    )

    print(f"\nPipeline 执行完成")
    print(f"成功: {result.get('success', False)}")
    if result.get('stdout'):
        print(f"输出:\n{result['stdout'][:500]}...")


# ============================================================================
# 示例 7: Parallel - 并行执行
# ============================================================================

async def example_parallel():
    """Parallel 编排示例"""
    from dslighting.operators.orchestration import Parallel
    from dslighting.operators.custom import SimpleOperator

    print("\n" + "=" * 80)
    print("示例 7: Parallel - 并行执行")
    print("=" * 80)

    # 创建多个模拟 Operators
    async def model_1(**kwargs):
        await asyncio.sleep(1)
        return {"model": "XGBoost", "score": 0.82}

    async def model_2(**kwargs):
        await asyncio.sleep(1.5)
        return {"model": "LightGBM", "score": 0.85}

    async def model_3(**kwargs):
        await asyncio.sleep(0.8)
        return {"model": "RandomForest", "score": 0.78}

    # 创建 Parallel
    parallel = Parallel([
        SimpleOperator(func=model_1),
        SimpleOperator(func=model_2),
        SimpleOperator(func=model_3)
    ], aggregation="best")

    # 执行
    import time
    start = time.time()
    result = await parallel.execute(data_dir="data/bike")
    duration = time.time() - start

    print(f"\n并行执行完成，耗时: {duration:.2f} 秒")
    print(f"最佳模型: {result['model']}")
    print(f"分数: {result['score']}")


# ============================================================================
# 示例 8: Conditional - 条件执行
# ============================================================================

async def example_conditional():
    """Conditional 编排示例"""
    from dslighting.operators.orchestration import Conditional
    from dslighting.operators.custom import SimpleOperator

    print("\n" + "=" * 80)
    print("示例 8: Conditional - 条件执行")
    print("=" * 80)

    # 定义分类和回归的 Operators
    async def classification_task(**kwargs):
        return {"task_type": "classification", "model": "LogisticRegression"}

    async def regression_task(**kwargs):
        return {"task_type": "regression", "model": "LinearRegression"}

    # 创建 Conditional
    conditional = Conditional(
        condition_fn=lambda ctx: ctx.get("task_type") == "classification",
        true_op=SimpleOperator(func=classification_task),
        false_op=SimpleOperator(func=regression_task)
    )

    # 测试分类任务
    print("\n测试 1: 分类任务")
    result1 = await conditional.execute(
        task="Predict customer churn",
        task_type="classification"
    )
    print(f"执行: {result1['task_type']}")
    print(f"模型: {result1['model']}")

    # 测试回归任务
    print("\n测试 2: 回归任务")
    result2 = await conditional.execute(
        task="Predict house price",
        task_type="regression"
    )
    print(f"执行: {result2['task_type']}")
    print(f"模型: {result2['model']}")


# ============================================================================
# 示例 9: 完整工作流
# ============================================================================

async def example_complete_workflow():
    """完整的数据分析工作流示例"""
    from dslighting.operators.orchestration import Pipeline
    from dslighting.operators import (
        PlanOperator,
        GenerateCodeAndPlanOperator,
        ExecuteAndTestOperator,
        ReviewOperator
    )
    from dsat.services.llm import LLMService
    from dslighting.services import SandboxService

    print("\n" + "=" * 80)
    print("示例 9: 完整数据分析工作流")
    print("=" * 80)

    # 初始化服务
    llm = LLMService()
    sandbox = SandboxService()

    # 创建完整工作流
    workflow = Pipeline([
        # Step 1: 制定计划
        PlanOperator(llm),

        # Step 2: 生成代码
        GenerateCodeAndPlanOperator(llm),

        # Step 3: 执行代码
        ExecuteAndTestOperator(sandbox),

        # Step 4: 审查结果
        ReviewOperator(llm)
    ])

    # 执行
    result = await workflow.execute(
        user_request="Load bike data, perform EDA, and train a simple model",
        data_dir="data/bike"
    )

    print(f"\n工作流执行完成")
    print(f"最终分数: {result.get('score', 'N/A')}")


# ============================================================================
# 主函数
# ============================================================================

async def main():
    """运行所有示例"""
    print("\n" + "=" * 80)
    print("DSLighting 内置 Operators 示例")
    print("=" * 80)

    # 运行示例
    await example_execute_and_test()
    # await example_plan()  # 需要真实的 LLM
    # await example_generate_code_and_plan()
    # await example_review()
    # await example_summarize()
    await example_pipeline()
    await example_parallel()
    await example_conditional()
    # await example_complete_workflow()

    print("\n" + "=" * 80)
    print("所有示例运行完成！")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
