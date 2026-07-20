#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量翻译 docfx 项目：
1. index.json 中的日文标题和摘要 → 中文
2. manifest.json 中的日文 Summary → 中文
3. HTML 文件中的英文大标题 → 中文 (English) 格式
"""
import json
import re
import os

BASE_DIR = r"d:\Program Files\0\AUOJ\auoj-user\Virial.Doc"

# ============================================================
# 1. 日文 → 中文 翻译字典
# ============================================================
JA_TO_ZH = {
    # 复合词（优先匹配）
    "幽霊役職": "幽灵职业", "モディファイア": "修改者",
    "割り当て器": "分配器", "割り当てテーブル": "分配表",
    "割り当てパラメータ": "分配参数", "割り当てルーチン": "分配流程",
    "役職定義": "职业定义", "役職カテゴリ": "职业类别",
    "役職フィルタ": "职业过滤器",
    "追加役職": "追加职业", "役職実体": "职业实例",
    "実行時役職": "运行时职业",
    "テキストアドオン": "脚本插件",
    "キル条件": "击杀条件", "キルクールダウン": "击杀冷却",
    "緊急会議": "紧急会议", "追放された": "被放逐",
    "コードネーム": "代码名称",
    "割り当てられる": "被分配",
    "拡張メソッド": "扩展方法",
    "コマンド文節": "命令短語",
    "シリアライズ": "序列化",
    "デシリアライズ": "反序列化",
    "一意に": "唯一地",
    "実行者": "执行者",
    "ハンドシェイク": "握手",
    "アサインメント": "分配",
    "プロパティ": "属性",
    "コンフィギュレーション": "配置",
    "インターフェース": "接口",
    "コンストラクタ": "构造函数",
    "インデクサー": "索引器",
    "オーバーロード": "重载",
    "オーバーライド": "重写",
    "フィールド": "字段",
    "コンテナ": "容器",
    "テンプレート": "模板",
    "エントリ": "条目",
    "フィルタ": "过滤器",
    "ハンドラ": "处理器",
    "ロガー": "记录器",
    "トラッカー": "追踪器",
    "タイマー": "计时器",
    "オーバーレイ": "覆盖层",
    "ファクトリ": "工厂",
    "プロバイダ": "提供者",
    "ビルダー": "构建器",
    "プロセッサ": "处理器",
    "デコレーター": "装饰器",
    "プロキシ": "代理",
    "アダプター": "适配器",
    "ラッパー": "包装器",
    "コールバック": "回调",
    "リスナー": "监听器",
    "エディター": "编辑器",
    "スキーマ": "概要",
    "オプション": "选项",
    "ドキュメント": "文档",
    "リソース": "资源",
    "レジストリ": "注册表",
    "キュー": "队列",
    "スタック": "栈",
    "セッション": "会话",
    "レポーター": "报告者",
    "ビューア": "查看器",
    "エクスポート": "导出",
    "インポート": "导入",
    # 游戏术语
    "インポスター": "内鬼", "クルーメイト": "船员",
    "クールダウン": "冷却时间", "ベント": "通风管",
    "キル": "击杀", "キル能力": "击杀能力",
    "緊急": "紧急", "ボタン": "按钮",
    "投票": "投票", "追放": "放逐",
    "死亡": "死亡", "生存": "生存",
    "死因": "死因", "殺人": "击杀",
    "殺害": "杀害", "復活": "复活", "蘇生": "复活",
    "無敵": "无敌", "透明": "透明",
    "視界": "视野", "速度": "速度",
    "移動": "移动", "出現": "出现",
    "陣営": "阵营", "開示": "公开",
    "推察": "推测", "推測": "推测",
    "試合": "比赛", "マップ": "地图",
    "ミニゲーム": "小游戏",
    "ラウンド": "回合", "フェーズ": "阶段",
    "タスク": "任务",
    # 通用技术词汇
    "プレイヤー": "玩家", "ゲーム": "游戏",
    "役職": "职业", "チーム": "队伍",
    "エンティティ": "实体", "パラメータ": "参数",
    "リターン": "返回", "戻り値": "返回值",
    "デフォルト": "默认", "デフォルト値": "默认值",
    "パラメータ値": "参数值",
    "インスタンス": "实例", "プロトタイプ": "原型",
    "クラス": "类", "列挙": "枚举",
    "デリゲート": "委托", "メソッド": "方法",
    "イベント": "事件", "定義": "定义",
    "実体": "实例", "実行時": "运行时",
    "割り当て": "分配",
    "定義済み": "已定义",
    "割り当てられた": "被分配的",
    "役職に": "职业的",
    "役職を": "职业",
    "プレイヤーに": "玩家的",
    "プレイヤーを": "玩家",
    "追跡": "追踪", "通知": "通知",
    "変換": "转换", "比較": "比较",
    "生成": "生成", "取得": "取得",
    "設定": "设置", "追加": "追加",
    "削除": "删除", "更新": "更新",
    "登録": "注册", "解除": "解除",
    "初期化": "初始化",
    "呼び出し": "调用",
    "呼び出される": "被调用",
    "使用する": "使用",
    "保持する": "保持", "提供する": "提供",
    "取得する": "取得", "設定する": "设置",
    "表す": "表示", "表します": "表示。",
    "記述": "描述", "記述する": "描述",
    "表記": "表达",
    "保持": "保持", "保持する": "保持",
    "管理": "管理", "操作": "操作",
    "処理": "処理", "確認": "确认",
    "評価": "评估", "判定": "判定",
    "追跡する": "追踪",
    "返す": "返回", "返します": "返回。",
    "含む": "含", "含みます": "含。",
    "含む場合": "含时",
    "実行": "执行", "実行する": "执行",
    "実行可能": "可执行",
    "使用": "使用", "使用される": "被使用",
    "作成": "创建", "作成する": "创建",
    "破棄": "Dispose",
    "更新する": "更新",
    "登録する": "注册",
    "解除する": "解除",
    "初期化する": "初始化",
    "通知する": "通知",
    "送信する": "发送", "受信する": "接收",
    "記憶する": "記憶",
    "評価する": "评估", "比較する": "比较",
    "変換する": "转换", "適用する": "适用",
    "呼び出す": "調用",
    "開く": "打开", "閉じる": "关闭",
    "ロック": "锁定",
    "バージョン": "版本", "リリース": "发布",
    "フォーマット": "格式",
    "オブジェクト": "对象",
    "関連": "相关", "関連付け": "関連",
    "使用法": "使用方法",
    "次の": "以下",
    "その": "该", "この": "此",
    "すべての": "所有",
    "対象": "对象",
    "値": "值", "状態": "状态",
    "コンテキスト": "上下文",
    "スコープ": "作用域",
    "デバッグ": "调试",
    "プロファイリング": "性能分析",
    "ログ": "日志",
    "エラー": "错误", "警告": "警告",
    "例外": "例外", "スロー": "抛出",
    "キャッチ": "捕获",
    "再試行": "重试",
    "タイムアウト": "超时",
    "ファイル": "文件", "フォルダ": "文件夹",
    "ディレクトリ": "目录", "パス": "路径",
    "一意": "唯一",
    "修飾子": "修饰符", "修飾": "修饰",
    "抽象": "抽象", "仮想": "虚",
    "継承": "继承", "実装": "实现",
    "静的": "静态", "公開": "公开",
    "有効": "有效", "無効": "无效",
    "有効な": "有效的", "無効な": "无效的",
    "アクティブな": "活跃的",
    "正常な": "正常的",
    "互換性": "兼容性",
    "廃止": "废弃", "非推奨": "已弃用",
    "注釈": "注解",
    "以下を参照": "参见", "以下の": "以下的",
    "ミリ秒": "毫秒", "刻み幅": "步长",
    "最小値": "最小值", "最大値": "最大值",
    "ステートメント": "语句",
    "コード": "代码",
    "配列": "数组", "トークン": "令牌",
    "コマンド": "命令",
    "補完候補": "补全候选",
    "マスク": "掩码", "ビット": "位",
    "ローカル": "本地", "リモート": "远程",
    "セーブ": "保存", "ロード": "加载",
    "無視": "忽略", "無視する": "忽略",
    "付随": "附属", "付与": "赋予",
    "簒奪": "篡夺", "簒奪可能": "可篡夺",
    "テンプレート": "模板",
    "プロセス": "进程",
    "スレッド": "线程",
    "デフォルト値": "默认值",
    "コンストラクター": "构造函数",
    # SuperNewRoles
    "貢献": "贡献", "ガイド": "指南",
    "開発環境": "开发环境", "セットアップ": "安装配置",
    "必要条件": "要求", "リポジトリ": "仓库",
    "インストール": "安装",
    "ビルド": "构建", "ソリューション": "解决方案",
    "ライセンス": "许可", "参照": "参考",
    "公式": "官方", "導入方法": "导入方法",
    "解析": "解析", "改善": "改善",
    "クレジット": "致谢", "支援": "支持",
    "情報": "信息", "一覧": "一览",
    "詳しい": "详细", "状況": "情况",
    "移行": "迁移", "矛盾": "矛盾",
    "古い": "旧版", "最新": "最新",
    "収集": "收集", "送信": "发送",
    "データ": "数据",
    "日本語": "日语", "英語": "英语",
    "お問い合わせ": "联系我们",
    "ご質問": "问题",
    "��要": "概要",
    # 贡献文档
    "クローン": "克隆",
    "インストールパス": "安装路径",
    "環境変数": "环境变量",
    "コマンド": "命令",
    "メソッド": "方法",
    "コンテナ": "容器",
    "ファクトリ": "工厂",
    "バージョン": "版本",
    "ファイル": "文件",
    "リポジトリ": "仓库",
    "オプション": "选项",
    "スクリプト": "脚本",
    "関連": "相关",
    "追跡器": "追踪器",
    "ハンドラ": "处理器",
    "フィルタ": "过滤器",
    "ファサード": "门面",
    "プロバイダ": "提供者",
    "モニター": "监视器",
    "スコープ": "作用域",
    "コンテナ": "容器",
    "リポジトリ": "仓库",
    "サービス": "服务",
    "アトリビュート": "属性",
    "アサイン": "分配",
    "フィルタリング": "过滤",
}

# ============================================================
# 2. 英文大标题 → 中文 (English) 翻译映射
# ============================================================
HEADING_ZH_MAP = {
    "Namespace": "命名空间",
    "Class": "类",
    "Interface": "接口",
    "Struct": "结构体",
    "Enum": "枚举",
    "Delegate": "委托",
    "Properties": "属性",
    "Methods": "方法",
    "Events": "事件",
    "Operators": "运算符",
    "Fields": "字段",
    "Returns": "返回值",
    "Type Parameters": "类型参数",
    "Field Value": "字段值",
    "Constructors": "构造函数",
    "Indexers": "索引器",
    "See Also": "另请参见",
    "Extension Methods": "扩展方法",
    "Implements": "实现",
    "Inherited": "继承",
    "Inherited Members": "继承成员",
    "Remarks": "备注",
    "Applies to": "适用范围",
    "Syntax": "语法",
    "Parameters": "参数",
    "Return value": "返回值",
    "Return Value": "返回值",
    "Property Value": "属性值",
    "Exceptions": "例外",
    "Examples": "示例",
    "Thread Safety": "线程安全",
    "Thread safety": "线程安全",
    "Version": "版本",
    "Definition": "定义",
    "Declarations": "声明",
    "Implementations": "实现",
    "Explicit Implementations": "显式实现",
    "Explicit Interface Implementations": "显式接口实现",
    "Usage": "用法",
    "See also": "另请参见",
    "Classes": "类",
    "Interfaces": "接口",
    "Structs": "结构体",
    "Delegates": "委托",
    "Enums": "枚举",
}


def translate_japanese_text(text):
    """将日文文本翻译为中文"""
    if not text:
        return text
    if not re.search(r'[\u3040-\u309F\u30A0-\u30FF]', text):
        return text
    result = text
    for ja, zh in sorted(JA_TO_ZH.items(), key=lambda x: -len(x[0])):
        result = result.replace(ja, zh)
    return result


def translate_index_json():
    """翻译 index.json"""
    filepath = os.path.join(BASE_DIR, "index.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    count = 0
    for key, entry in data.items():
        for field in ["title", "summary"]:
            if field in entry and entry[field]:
                new_val = translate_japanese_text(entry[field])
                if new_val != entry[field]:
                    entry[field] = new_val
                    count += 1
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[index.json] 翻译了 {count} 处")
    return count


def translate_manifest_json():
    """翻译 manifest.json"""
    filepath = os.path.join(BASE_DIR, "manifest.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    count = 0
    if "files" in data:
        for entry in data["files"]:
            if "Summary" in entry and entry["Summary"]:
                new_val = translate_japanese_text(entry["Summary"])
                if new_val != entry["Summary"]:
                    entry["Summary"] = new_val
                    count += 1
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[manifest.json] 翻译了 {count} 处")
    return count


def translate_html_headings(html_content):
    """将HTML中的英文内容翻译为「中文 (English)」格式"""
    new_content = html_content

    # 1. 翻译 <h1> 标签：如 "Namespace Virial.Xxx" → "命名空间 (Namespace) Virial.Xxx"
    for en, zh in HEADING_ZH_MAP.items():
        pattern = re.compile(
            r'(<h1[^>]*>\s*)' + re.escape(en) + r'(\s+)',
            re.MULTILINE
        )
        replacement = r'\g<1>' + zh + ' (' + en + r')\2'
        new_content = pattern.sub(replacement, new_content)

    # 2. 翻译 h2/h3/h4 标签内容
    for en, zh in HEADING_ZH_MAP.items():
        translated = zh + " (" + en + ")"
        pattern = re.compile(
            r'(<h[234]\s+[^>]*>\s*)' + re.escape(en) + r'(\s*</h[234]>)',
            re.MULTILINE | re.DOTALL
        )
        new_content = pattern.sub(r'\g<1>' + translated + r'\2', new_content)

    # 3. 翻译 <dt> 标签中的英文标签
    DT_ZH_MAP = {
        "Namespace": "命名空间 (Namespace)",
        "Inheritance": "继承 (Inheritance)",
        "Implements": "实现 (Implements)",
        "Derived": "派生 (Derived)",
        "Extension Methods": "扩展方法 (Extension Methods)",
        "Inherited Members": "继承成员 (Inherited Members)",
        "Inherited": "继承 (Inherited)",
    }
    for en, translated in DT_ZH_MAP.items():
        pattern = re.compile(
            r'(<dt>)\s*' + re.escape(en) + r'\s*(</dt>)',
            re.MULTILINE
        )
        new_content = pattern.sub(r'\g<1>' + translated + r'\2', new_content)

    # 4. 翻译 UI 元素
    UI_MAP = {
        'title="View source"': 'title="查看源代码 (View source)"',
        'placeholder="Search"': 'placeholder="搜索 (Search)"',
        'placeholder="Filter by title"': 'placeholder="按标题筛选 (Filter by title)"',
        '>Table of Contents<': '>目录 (Table of Contents)<',
        'aria-label="Close"': 'aria-label="关闭 (Close)"',
        'aria-label="Search"': 'aria-label="搜索 (Search)"',
        'aria-label="Toggle navigation"': 'aria-label="切换导航 (Toggle navigation)"',
        'aria-label="Show table of contents"': 'aria-label="显示目录 (Show table of contents)"',
    }
    for en, zh in UI_MAP.items():
        new_content = new_content.replace(en, zh)

    # 5. 翻译 <meta name="loc:..."> 标签内容（这些被 JS 用于 UI 显示）
    META_MAP = {
        'content="In this article"': 'content="本文内容 (In this article)"',
        'content="{count} results for &quot;{query}&quot;"': 'content="找到 {count} 个结果 &quot;{query}&quot; ({count} results for &quot;{query}&quot;)"',
        'content="No results for &quot;{query}&quot;"': 'content="无结果 &quot;{query}&quot; (No results for &quot;{query}&quot;)"',
        'content="Filter by title"': 'content="按标题筛选 (Filter by title)"',
        'content="Next"': 'content="下一页 (Next)"',
        'content="Previous"': 'content="上一页 (Previous)"',
        'content="Light"': 'content="浅色 (Light)"',
        'content="Dark"': 'content="深色 (Dark)"',
        'content="Auto"': 'content="自动 (Auto)"',
        'content="Change theme"': 'content="切换主题 (Change theme)"',
        'content="Copy"': 'content="复制 (Copy)"',
        'content="Download PDF"': 'content="下载 PDF (Download PDF)"',
    }
    for en, zh in META_MAP.items():
        new_content = new_content.replace(en, zh)

    return new_content


def translate_all_html():
    """遍历所有HTML文件，翻译大标题"""
    count = 0
    for dirpath in ["api", "docs", "SuperNewRoles", ""]:
        base = os.path.join(BASE_DIR, dirpath) if dirpath else BASE_DIR
        for root, dirs, files in os.walk(base):
            for fname in files:
                if not fname.endswith(".html"):
                    continue
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception:
                    continue
                new_content = translate_html_headings(content)
                if new_content != content:
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    count += 1
    print(f"[HTML] 翻译了 {count} 个文件的标题")
    return count


if __name__ == "__main__":
    print("=" * 50)
    print("开始批量翻译")
    print("=" * 50)
    translate_index_json()
    translate_manifest_json()
    translate_all_html()
    print("=" * 50)
    print("翻译完成！")
    print("=" * 50)
