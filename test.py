# -*- coding: utf-8 -*-
'''
File Name: test.py
Author: JackeyGao
mail: junqi.gao@shuyun.com
Created Time: 一  7/ 6 17:40:15 2015
'''

from cmdbws import Cmdbws
from cmdbws import printj

if __name__ == '__main__':
    url = "http://cmdb.example.com/services/rest/v1"
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

