#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/5/9 15:49
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

import matplotlib.pyplot as plt  #######
#
# def plot_lift_curve(predictions, labels, threshold_list, cut_point=100):
#     base = len([x for x in labels if x == 1]) / len(labels)
#     predictions_labels = list(zip(predictions, labels))
#     lift_values = []
#
#     x_axis_range = np.linspace(0, 1, cut_point)
#     x_axis_valid = []
#     for i in x_axis_range:
#         hit_data = [x[1] for x in predictions_labels if x[0] > i]
#         if hit_data:  # 避免为空
#             bad_hit = [x for x in hit_data if x == 1]
#             precision = len(bad_hit) / len(hit_data)
#             lift_value = precision / base
#             lift_values.append(lift_value)
#             x_axis_valid.append(i)
#
#     plt.plot(x_axis_valid, lift_values, color="blue")  # 提升线
#     plt.plot([0, 1], [1, 1], linestyle="-", color="darkorange", alpha=0.5, linewidth=2)  # base线
#
#     for threshold in threshold_list:
#         threshold_hit_data = [x[1] for x in predictions_labels if x[0] > threshold]
#         if threshold_hit_data:
#             threshold_bad_hit = [x for x in threshold_hit_data if x == 1]
#             threshold_precision = len(threshold_bad_hit) / len(threshold_hit_data)
#             threshold_lift_value = threshold_precision / base
#             plt.scatter([threshold], [threshold_lift_value], color="white", edgecolors="blue", s=20,
#                         label="threshold:{} lift:{}".format(threshold, round(threshold_lift_value)), value, 2)))  # 阈值点
#             plt.plot([threshold, threshold], [0, 20], linestyle="--", color="black", alpha=0.2, linewidth=1)  # 阈值的纵轴
#             plt.text(threshold - 0.02, threshold_lift_value + 1, round(threshold_lift_value, 2))
#             plt.title("Lift plot")
#             plt.legend(loc=2, prop={"size": 9})
#             plt.grid()
#             plt.show()


