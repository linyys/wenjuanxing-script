# wenjuanxing-script
## ·使用前
#### 需要```python3.x```环境
#### 运行```pip install selenium```
#### 修改```config.json```配置
#### 添加```main.py```中的```url```变量
#### 运行```main.py```文件

## ·```config.json```配置参数
```
t-type(number)  1: 单选题
                2: 多选题
                3: 矩阵题
                4: 滑动
                5: 填空
                6: 排序
                7: 量表
--------------------------
gai_lv(array) 每个选项的选中概率(数组长度需与选项匹配)
```
特殊题型的特殊参数参考以下示例
```
示例：
{
    "configs": [
        {
            "t-type" : 1,
            "gai_lv": [0.3, 0.2, 0.5]
        },
        {
            "t-type" : 1,
            "gai_lv": [0.3, 0.2, 0.5]
        },
        {
            "t-type": 2,
            "option": 2,        选中选项的数量
            "gai_lv": [0.3, 0.2, 0.5]
        },
        {
            "t-type": 3,
            "topic_nums": 6,    小题数量
            "gai_lv": [0.3, 0.2, 0.2, 0.1, 0.2]
        },
        {
            "t-type": 4,
            "intervals": [0, 50]    选择区间
        }
    ]
}
```