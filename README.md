# cmdbws
Client of cmdbuild rest service 


## Usage

```python
from cmdbws import Cmdbws
from cmdbws import printj

if __name__ == '__main__':
    url = "http://example.com/services/rest/v1"
    cmdb = Cmdbws(url, "admin", "xxxxxxxxx")
    table = cmdb.get_class("config")

    # class 信息
    printj(table.info)
    printj(table.attributes)
    printj(table.lookups)
    printj(table.references)

    # 查询所有
    printj(table.list())

    data = {
            "product": "BI",
            "srm_id": 4261,
            "notify_method": "TICK",
            "contacts": "junqi.gao",
            "is_valid": True,
            "Description": "test",
            "leader": "junqi.gao"
            }
    # 增加
    card_id = table.create(data)
    
    data["srm_id"] = 426
    
    # 更新
    print(table.update(card_id, data))

    # 查询单个
    print(table.status(card_id))

    # 删除
    print(table.delete(card_id))

```

## Function

* 支持class card增删改查
* 支持lookup-type 自动转换
* 支持reference 自动转换
* 用户名密码认证

## Future

* 暂无


## License

The MIT License (MIT)

Copyright (c) 2015 JackeyGao

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

