from yplib import *
from yplib.index import *


def get_space_count(s: str = '',
                    use_start_index: int = 0,
                    html_data: str = None,
                    key: str = None) -> int:
    """
    # 以 \n 作为分隔符，计算左边的空格的最小长度
    # use_start_index : 开始使用的 index
    """
    if html_data is None:
        # 提取非空行，计算每行前导空格数，并返回其中的最小值
        return min((len(line) - len(line.lstrip(' ')) for line in str(s)[use_start_index:].split('\n') if line.strip()), default=0)
    i = html_data.find(key)
    while i >= 0 and html_data[i] != '\n':
        i -= 1
    c = 0
    while i < len(html_data) and html_data[i].isspace():
        i += 1
        c += 1
    if c > 0:
        c -= 1
    return c


def get_space(s: int | str = None,
              use_start_index: int = 0,
              html_data: str = None,
              key: str = None) -> str:
    """
    # 获得 指定数量 的 空格
    # s                 : 字符串, 当传入这个参数的时候, 意思是：去掉 以 \n 作为换行符，去掉每一行公共的 空格
    # use_start_index   : 开始使用的 index
    # html_data         : html 字符串
    # key               : html 中的 key
    """
    if isinstance(s, int):
        return ' ' * int(s)
    return ' ' * get_space_count(s, use_start_index=use_start_index, html_data=html_data, key=key)


# 去掉字符串开头和结尾的换行符（如果存在）
def strip_n(s: str) -> str:
    s = s.strip()
    if s.startswith('\n') or s.endswith('\n'):
        return s.strip('\n')
    return s.strip()


# 使用 echarts 的基本图表
def to_chart_html(option: str) -> str:
    uid = random_letter(is_upper=True)
    s = '''
        <!DOCTYPE html>
        <html lang="zh-CN" style="background: #100c2a;height: 100%;">
        <head>
            <meta charset="utf-8">
            <link rel="shortcut icon" href="https://echarts.apache.org/favicon.ico" type="image/x-icon">
            <title>-chart_name- - Apache ECharts</title>
        </head>
        <body style="height: calc(100% - 40px);margin: 0;">
        <div id="container-uid-" style="height: 100%;margin: 20px;"></div>
        <script type="text/javascript" src="https://fastly.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
        <script type="text/javascript">
            var option-uid- = -option-;
            var myChart-uid- = echarts.init(document.getElementById("container-uid-"), "dark", {
                renderer: "canvas",
                useDirtyRect: false,
            });
            myChart-uid-.setOption(option-uid-);
            window.addEventListener("resize", myChart-uid-.resize);
            console.log("option = " + JSON.stringify(option-uid-));
        </script>
        </body>
        </html>
        '''
    return (
        s.strip()
        .replace('\n' + get_space(s), '\n')
        .replace('-option-', str(option))
        .replace('-uid-', uid)
    )


# 使用 table 的基本图表
def to_table_list_html(table_list: list,
                    header_obj: list,
                    title: str) -> str:
    uid = random_letter(is_upper=True)
    s = '''
        <!DOCTYPE html>
        <html lang="zh-CN" style="height: 100%;">
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
        </head>
        <body style="height: calc(100% - 40px);margin: 0;">
        <div id="app-uid-" style="height: 100%;margin: 20px;">
            <el-row style="padding: 10px;">
                <el-col :span="12" style="text-align: right;">
                    <span style="font-size: 1.5em;font-weight: bold;">-title-</span>
                </el-col>
                <el-col :span="12" style="text-align: right;">
                    <el-button type="primary" size="small" @click="export_csv()">Export CSV</el-button>
                </el-col>
            </el-row>
            <el-table
                    :data="tableData-uid-"
                    border
                    stripe
                    max-height="850"
                    style="width: 100%">
                <el-table-column label="Index" type="index" fixed width="50"></el-table-column>
                <el-table-column v-for="(value, key, index) of header-uid-" :key="index"
                                 :fixed="index===0" sortable :prop="key" :label="value">
                </el-table-column>
            </el-table>
        </div>
        </body>
        <script src="https://unpkg.com/vue@2/dist/vue.js"></script>
        <script src="https://unpkg.com/element-ui/lib/index.js"></script>
        <script>
            new Vue({
                el: "#app-uid-",
                data: function () {
                    return {
                        header-uid-: {
                            -header_obj-
                        },
                        tableData-uid-: [
                            -table_list-
                        ]
                    }
                },
                methods: {
                    export_csv() {
                        let list = []
                        let date = new Date();
                        let name = `${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}${String(date.getDate()).padStart(2, '0')}_`
                            + `${String(date.getHours()).padStart(2, '0')}${String(date.getMinutes()).padStart(2, '0')}${String(date.getSeconds()).padStart(2, '0')}`;
                        let first = []
                        for (let k of Object.keys(this.header-uid-)) {
                            first.push(this.header-uid-[k])
                        }
                        list.push(first)
                        this.tableData-uid-.map(t => {
                            let line = []
                            for (let k of Object.keys(this.header-uid-)) {
                                line.push(t[k])
                            }
                            list.push(line)
                        })
                        const newList = list.map(res => res.join(","))
                        const data = newList.join(",\\n")
                        var uri = "data:text/csv;charset=utf-8,\\ufeff" + encodeURIComponent(data);
                        var downloadLink = document.createElement("a");
                        downloadLink.href = uri;
                        downloadLink.download = (name + ".csv") || "temp.csv";
                        document.body.appendChild(downloadLink);
                        downloadLink.click();
                        document.body.removeChild(downloadLink);
                    }
                }
            })
        </script>
        </html>
    '''
    total_space_count = get_space_count(s)
    total_space = get_space(total_space_count)
    return (
        s.strip()
        .replace('\n' + total_space, '\n')
        .replace('-header_obj-',
                 (',\n' + get_space(get_space_count(html_data=s, key='-header_obj-') - total_space_count)).join(header_obj))
        .replace('-title-', title)
        .replace('-table_list-',
                 (',\n' + get_space(get_space_count(html_data=s, key='-table_list-') - total_space_count)).join(table_list))
        .replace('-uid-', uid)
    )


# 使用 text 的基本图表
def to_text_list_html(text_list: list,
                      title: str) -> str:
    uid = random_letter(is_upper=True)
    s = '''
        <!DOCTYPE html>
        <html lang="zh-CN" style="height: 100%;">
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
        </head>
        <body style="height: calc(100% - 40px);margin: 0;">
        <div id="app-uid-" style="height: 100%;margin: 20px;">
            <el-row style="padding: 10px;">
                <el-descriptions :title="title" :column="1" direction="vertical">
                    <el-descriptions-item v-for="(obj, index) of text_list" :key="index" :label="obj['name']">
                        {{obj['text']}}
                    </el-descriptions-item>
                </el-descriptions>
            </el-row>
        </div>
        </body>
        <script src="https://unpkg.com/vue@2/dist/vue.js"></script>
        <script src="https://unpkg.com/element-ui/lib/index.js"></script>
        <script>
            new Vue({
                el: "#app-uid-",
                data: function () {
                    return {
                        title: "-title-",
                        text_list: -text_list-
                    }
                }
            })
        </script>
        </html>
    '''
    total_space_count = get_space_count(s)
    text_space_count = get_space_count(html_data=s, key='-text_list-') - total_space_count
    text_space = get_space(text_space_count + 4)
    text_space_suffix = get_space(text_space_count)
    text_list_str = '\n' + text_space + (',\n' + text_space).join(text_list) + '\n' + text_space_suffix
    return (
        s.strip()
        .replace('\n' + get_space(total_space_count), '\n')
        .replace('-text_list-', f"[{text_list_str}]")
        .replace('-title-', str(title))
        .replace('-uid-', uid)
    )


# 折线图的 html 模板代码
def to_line_stack_html() -> str:
    option = '''
    {
        title: {
            text: "-chart_name-",
        },
        tooltip: {
            trigger: "axis",
        },
        dataZoom: [
            {
                show: true,
                realtime: true,
            },
            {
                type: "inside",
                realtime: true,
            },
        ],
        grid: {
            left: "30px",
            right: "30px",
            bottom: "50px",
            containLabel: true,
        },
        toolbox: {
            feature: {
                saveAsImage: {
                    pixelRatio: 5
                },
            },
        },
        yAxis: {
            type: "value",
            scale: true
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: -x_list-,
        },
        legend: -legend-,
        series: -series-,
    }
    '''
    s = strip_n(option)
    return to_chart_html(s.replace('\n' + get_space(get_space_count(s, 1) - 4), '\n'))


# 折线图的 html 模板代码
def to_line_area_html() -> str:
    option = '''
    {
        tooltip: {
            trigger: "axis",
        },
        title: {
            text: "-chart_name-"
        },
        toolbox: {
            feature: {
                saveAsImage: {
                    pixelRatio: 5
                },
            }
        },
        grid: {
            left: "30px",
            right: "30px",
            bottom: "50px",
            containLabel: true,
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: -x_list-
        },
        yAxis: {
            type: "value",
            scale: true
        },
        dataZoom: [
            {
                show: true,
                realtime: true,
            },
            {
                type: "inside",
                realtime: true,
            },
        ],
        series: [
            {
                type: "line",
                symbol: "none",
                smooth: -smooth-,
                sampling: "lttb",
                itemStyle: {
                    color: "rgb(255, 70, 131)"
                },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                          offset: 0,
                          color: "rgb(255, 158, 68)"
                        },
                        {
                          offset: 1,
                          color: "rgb(255, 70, 131)"
                        }
                    ])
                },
                data: -y_list-
            }
        ]
    }
    '''
    s = strip_n(option)
    return to_chart_html(s.replace('\n' + get_space(get_space_count(s, 1) - 4), '\n'))


# 饼图的 html 模板代码
def to_pie_html() -> str:
    option = '''
    {
        title: {
            text: "-chart_name-",
            left: 10
        },
        tooltip: {
            trigger: "item"
        },
        toolbox: {
            feature: {
                saveAsImage: {
                    pixelRatio: 5
                },
            },
        },
        legend: {
            top: "5%",
            left: "center"
        },
        series: [
            {
                name: "-chart_name-",
                type: "pie",
                radius: ["30%", "70%"],
                itemStyle: {
                    borderRadius: 10,
                    borderColor: "#fff",
                    borderWidth: 1
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 30,
                        fontWeight: "bold"
                    }
                },
                labelLine: {
                    show: true
                },
                data: -x_list-
            }
        ]
    }
    '''
    s = strip_n(option)
    return to_chart_html(s.replace('\n' + get_space(get_space_count(s, 1) - 4), '\n'))


# 柱状的 html 模板代码
def to_bar_html() -> str:
    option = '''
    {
        title: {
            text: "-chart_name-",
            left: 10
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: false
                },
                saveAsImage: {
                    saveAsImage: {
                        pixelRatio: 5
                    },
                }
            }
        },
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow"
            }
        },
        grid: {
            left: "30px",
            right: "30px",
            bottom: "50px",
            containLabel: true,
        },
        dataZoom: [
            {
              type: "inside"
            },
            {
              type: "slider"
            }
        ],
        xAxis: {
            data: -x_list-,
            silent: false,
            splitLine: {
                show: false
            },
            splitArea: {
                show: false
            }
        },
        yAxis: {
            splitArea: {
                show: false
            },
            scale: true
        },
        series: [
            {
                type: "bar",
                data: -y_list-,
                large: true
            }
        ]
    }
    '''
    s = strip_n(option)
    return to_chart_html(s.replace('\n' + get_space(get_space_count(s, 1) - 4), '\n'))


# 性能分析图的 html 模板代码
def to_gantt_html() -> str:
    option = '''
    {
        tooltip: {
            formatter: function (params) {
                return params.marker + params.name
                    + "</br>"
                    + "<table style='width:100%;'>"
                    + "<tr><td style='width:70px;'>Start:</td><td>" + params.value[1] + "</td></tr>"
                    + "<tr><td style='width:70px;'>End:</td><td>" + params.value[2] + "</td></tr>"
                    + "<tr><td style='width:70px;'>Duration:</td><td>" + params.value[3] + "</td></tr>"
                    + "</table>";
            }
        },
        title: {
            text: "-chart_name-",
        },
        dataZoom: [
            {
                type: "slider",
                filterMode: "weakFilter",
                showDataShadow: false,
                labelFormatter: ""
            },
            {
                type: "inside",
                filterMode: "weakFilter"
            }
        ],
        grid: {
            left: "30px",
            right: "30px",
            bottom: "50px",
            containLabel: true,
        },
        xAxis: {
            scale: true,
            min: -x_min-,
            max: -x_max-
        },
        yAxis: {
            data: -y_list-
        },
        series: [
            {
                type: "custom",
                renderItem: function (params, api) {
                    var categoryIndex = api.value(0);
                    var start = api.coord([api.value(1), categoryIndex]);
                    var end = api.coord([api.value(2), categoryIndex]);
                    var height = api.size([0, 1])[1] * 0.6;
                    var rectX = Math.max(start[0], params.coordSys.x);
                    var rectWidth = Math.min(end[0], params.coordSys.x + params.coordSys.width) - rectX;
                    var r = Math.max(height / 5, 5);
                    var fz = Math.max(height / 5, 15);
                    var fontSize = Math.max(rectWidth / 10, 2);
                    fontSize = Math.min(fontSize, fz);
                    var textX = rectX + rectWidth / 2;
                    var textY = start[1];
                    return {
                        type: 'group',
                        children: [
                            {
                                type: "rect",
                                shape: {
                                    x: rectX,
                                    y: start[1] - height / 2,
                                    width: rectWidth,
                                    height: height,
                                    r: [r, r, r, r]
                                },
                                style: api.style()
                            },
                            {
                                type: 'text',
                                style: {
                                    text: api.value(4),
                                    x: textX,
                                    y: textY,
                                    textAlign: 'center',
                                    textVerticalAlign: 'middle',
                                    fill: '#fff',
                                    fontWeight: 'bold',
                                    fontSize: fontSize
                                }
                            }
                        ]
                    };
                },
                itemStyle: {
                    opacity: 0.8
                },
                encode: {
                    x: [1, 2],
                    y: 0
                },
                data: -x_list-
            }
        ]
    }
    '''
    s = strip_n(option)
    return to_chart_html(s.replace('\n' + get_space(get_space_count(s, 1) - 4), '\n'))
