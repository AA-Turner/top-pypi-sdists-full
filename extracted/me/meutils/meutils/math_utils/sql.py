#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : sql
# @Time         : 2025/9/24 21:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import calendar
import sys


def generate_partition_script_by_dates(start_date_str, end_date_str):
    """
    根据开始和结束日期生成MySQL RANGE分区脚本

    Args:
        start_date_str: 开始日期，格式 'YYYY-MM-DD'
        end_date_str: 结束日期，格式 'YYYY-MM-DD'

    Returns:
        str: 完整的分区SQL脚本
    """
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError as e:
        raise ValueError(f"日期格式错误，请使用 YYYY-MM-DD 格式: {e}")

    if start_date > end_date:
        raise ValueError("开始日期不能晚于结束日期")

    # 生成所有日期
    current_date = start_date
    dates = []
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)

    # 生成分区定义
    partition_lines = []
    for date in dates:
        partition_name = f"p{date.strftime('%Y%m%d')}"
        next_day = date + timedelta(days=1)
        next_day_str = next_day.strftime('%Y-%m-%d')
        partition_line = f"  PARTITION {partition_name} VALUES LESS THAN (UNIX_TIMESTAMP('{next_day_str} 00:00:00'))"
        partition_lines.append(partition_line)

    # 添加兜底分区
    partition_lines.append("  PARTITION pmax VALUES LESS THAN MAXVALUE")

    # 组装完整SQL
    sql_script = "ALTER TABLE logs\nPARTITION BY RANGE (created_at) (\n" + ",\n".join(partition_lines) + "\n);"

    return sql_script


def generate_partition_script_by_month(year, month):
    """
    根据年份和月份生成该月的分区脚本

    Args:
        year: 年份 (int)
        month: 月份 (int, 1-12)

    Returns:
        str: 完整的分区SQL脚本
    """
    if not (1 <= month <= 12):
        raise ValueError("月份必须在 1-12 之间")

    # 获取该月的天数
    days_in_month = calendar.monthrange(year, month)[1]

    start_date = f"{year:04d}-{month:02d}-01"
    end_date = f"{year:04d}-{month:02d}-{days_in_month:02d}"

    return generate_partition_script_by_dates(start_date, end_date)


def main():
    """主函数，提供交互式界面"""
    print("MySQL 分区脚本生成器")
    print("=" * 30)
    print("1. 按日期范围生成 (YYYY-MM-DD 到 YYYY-MM-DD)")
    print("2. 按月份生成 (年份 月份)")

    try:
        choice = input("\n请选择生成方式 (1 或 2): ").strip()

        if choice == "1":
            start_date = input("请输入开始日期 (YYYY-MM-DD): ").strip()
            end_date = input("请输入结束日期 (YYYY-MM-DD): ").strip()
            script = generate_partition_script_by_dates(start_date, end_date)

        elif choice == "2":
            year = int(input("请输入年份 (如 2025): "))
            month = int(input("请输入月份 (1-12): "))
            script = generate_partition_script_by_month(year, month)

        else:
            print("无效选择！")
            return

        # 输出结果
        print("\n" + "=" * 50)
        print("生成的分区脚本:")
        print("=" * 50)
        print(script)

        # 询问是否保存到文件
        save_choice = input("\n是否保存到文件? (y/n): ").strip().lower()
        if save_choice == 'y':
            filename = input("请输入文件名 (默认: partitions.sql): ").strip()
            if not filename:
                filename = "partitions.sql"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(script)
            print(f"脚本已保存到: {filename}")

    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n错误: {e}")


if __name__ == "__main__":
    # 按日期范围生成
    script = generate_partition_script_by_dates('2025-12-12', '2027-01-01')
    print(script)

    # 按月份生成
    # script = generate_partition_script_by_month(2025, 10)  # 2025年10月

    """
    -- 1. 创建新表（带合理分区）
    CREATE TABLE logs_new LIKE logs;
    -- 手动添加按月分区定义（如上）
    
    -- 2. 逐步迁移数据（按天/按小时）
    INSERT INTO logs_new 
    SELECT * FROM logs 
    WHERE created_at > UNIX_TIMESTAMP('2025-09-24 00:00:00');
    
    -- 3. 应用双写 or 停写切换
    RENAME TABLE logs TO logs_old, logs_new TO logs;

    SELECT count(1) FROM `logs` WHERE created_at > UNIX_TIMESTAMP('2025-09-24 00:00:00')
    """