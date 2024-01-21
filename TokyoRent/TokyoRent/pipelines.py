# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TokyorentPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name == 'price':
                value = adapter.get(field_name)
                adapter[field_name] = value[0][1:]
            elif field_name == 'size':
                value = adapter.get(field_name)
                adapter[field_name] = value[0][:-3]
            elif field_name == 'deposite':
                value = adapter.get(field_name)
                adapter[field_name] = value[0][1:]
            elif field_name == 'key_money':
                value = adapter.get(field_name)
                adapter[field_name] = value[0][1:]
            elif field_name == 'floor':
                value = adapter.get(field_name)
                if value[0]:
                    value = value[0]
                    first = value[:value.index('/')].strip()
                    second = value[value.index('/')+2:-1]
                    adapter[field_name] = [first, second]
                else:
                    adapter[field_name] = '' 
        
        return item

