import re
import os

API_DIR = 'api'

# 属性名称翻译映射
PROPERTY_MAP = {
    # AllocationParameters
    "OtherCost": "OtherCost (其他成本)",
    "OthersAssignment": "OthersAssignment (其他分配)",
    "ExtraAssignment": "ExtraAssignment (额外分配)",
    "ExtraAssignmentInfo": "ExtraAssignmentInfo (额外分配信息)",
    "CategoryOption": "CategoryOption (类别选项)",
    "GhostAllocator": "GhostAllocator (幽灵分配器)",
    "SwapType": "SwapType (交换类型)",
    "Task": "Task (任务)",
    "LabelType": "LabelType (标签类型)",
    "OutfitId": "OutfitId (外观ID)",
    "ExtraDeadInfo": "ExtraDeadInfo (额外死亡信息)",
    "PermissionVariable": "PermissionVariable (权限变量)",
    "SchedulableEventContext": "SchedulableEventContext (可调度事件上下文)",
    "OneLineTextElement": "OneLineTextElement (单行文本元素)",
}

count = 0

for root, dirs, files in os.walk(API_DIR):
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            modified = False
            
            for original, translated in PROPERTY_MAP.items():
                # 匹配 <h3> 标签内的属性名称
                pattern = re.compile(
                    r'(<h3\s+id="[^"]*"\s+data-uid="[^"]*">)\s*' + re.escape(original) + r'\s*(</h3>)',
                    re.DOTALL
                )
                
                if pattern.search(content):
                    content = pattern.sub(r'\g<1>' + translated + r'\g<2>', content)
                    modified = True
                    count += 1
            
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

print(f'属性名称翻译完成，共翻译 {count} 处')
