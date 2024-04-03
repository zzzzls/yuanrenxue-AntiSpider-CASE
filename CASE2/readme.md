## CASE2: CSS 字体加密「每次请求更换字体」

原理:

- 使用 fontTools 库，每次请求生成一份新的加密字体文件

- 替换网页中的 0-9 a-z A-Z



![](../assert/img/iShot_2024-04-04_04.46.52.jpg)





### Usage

```
docker build -t case1:0.0.1 .
docker run --rm -p 80:9242 case1:0.0.1
```







