"""布尔类型转换与真值判定示例."""

x = True
print(x)
print(type(x))

# 数值型真值测试（非零为 True，零为 False）
print(bool(14), bool(0.0))

# 字符串真值测试（非空为 True，空为 False）
print(bool("non_empty_string"), bool(''))
