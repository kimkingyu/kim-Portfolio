"""变量赋值、数据类型检查与内存标识符 (id) 示例."""

sample_id = entity_no = 8
item_label = 'image_sample_01'
item_tag = "feature_tag_a"

# 检查变量数据类型
print(type(item_label))
print(type(item_tag))

# 检查对象内存地址
print(id(sample_id), id(entity_no))
