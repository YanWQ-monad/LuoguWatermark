# 洛谷水印减弱工具

~~只要 998，洛谷水印带回家~~  
你是否已经正在为洛谷的水印而烦恼，除了设立“水印专区”（[如图](https://cdn.luogu.org/upload/pic/32038.png)）外，你现在还可以采用洛谷水印减弱工具。~~只要 998，~~ 就可以减弱（甚至抵消）水印！

## 特性

图片经过处理后（得到掩码图），再上传到洛谷图床，可以在一定程度上减弱水印（对于某些图片还可以抵消，见下文）。

这里有几个例子（基于洛谷 3.0）：

![Example 1](https://raw.githubusercontent.com/YanWQ-monad/static/master/LuoguWatermark/1.png)

![Example 2](https://raw.githubusercontent.com/YanWQ-monad/static/master/LuoguWatermark/2.png)

洛谷图床参考：Example [1](https://cdn.luogu.org/upload/pic/42381.png) [2](https://cdn.luogu.org/upload/pic/42407.png)（洛谷有 Referer 检测，请手动复制链接）

## 使用

**[在线体验](https://lg-watermark.monadx.com)**

### 依赖

首先确保你已安装了 Python，再安装依赖：

```
pip install Pillow
```

然后请 clone 本项目（其实只需要 `convert.py` 和 `base_black.png`, `base_white.png`）或下载[压缩包](https://github.com/YanWQ-monad/LuoguWatermark/archive/master.zip)。

```
git clone https://github.com/YanWQ-monad/LuoguWatermark.git
```

### 使用方法

请进入到 `convert.py` 所在目录，执行：

```
python convert.py [origin] [target]
```

其中 `[origin]` 为图片源文件，`[target]` 为输出文件名。

运行后它会输出一个期望相似值（见下文）

## 关于结果

**洛谷水印减弱工具会减弱水印，但并不保证能完全消除水印。**

> **这一段的数据由于洛谷更新已经失效**，~~仅供观光~~
> 
> 经过研究发现，RGB 在一定的范围内可以抵消水印：
>
> - R: \[0, 142\]
> - G: \[44, 187\]
> - B: \[112, 254\]
>
> 即如下图所示：
>
> <details>
>   <summary>点击查看</summary>
>   <img src="https://raw.githubusercontent.com/YanWQ-monad/static/master/LuoguWatermark/3.png" alt="Condition" />
> </details>

在其它情况下，此工具可以尽可能地减弱水印。

此时，工具会输出一个 `Difference` 值，即经过处理后的图像上传到洛谷后，与原图的区别的期望值（计算方式为期望 RGB 距离的平方和）。

该期望相似度可以用于判断去水印的效果（越小越好）。

上面例子的期望相似度：

> 注：这是洛谷 3.0 的数据

- 例 1：0.022121
- 例 2：8.905619

一般来说：

| 相似度 | 效果 |
|:---:|:---:|
| < 0.5 | 肉眼难以分辨 |
| 0.5 ~ 10 | 依稀可见 |
| > 10 | 应该只能变淡 |
