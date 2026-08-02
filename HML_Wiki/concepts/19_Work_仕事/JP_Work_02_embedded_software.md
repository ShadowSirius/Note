---
extends:
  - "[[JP_Vocab_09_work_school]]"
sibling_of:
  - "[[JP_Work_01_electrical_power]]"
  - "[[JP_Work_03_engineering_actions]]"
---
# 工程詞彙 02：嵌入式與軟體

## 🧠 記憶鉤
- **送受對稱**：送信(そうしん,發送)⇔受信(じゅしん,接收)是一組完全對稱的漢字組合詞，「送」與「受」互為反義字首，「信」代表訊號/訊息——記住這個結構後，入力(にゅうりょく,輸入)⇔出力(しゅつりょく,輸出)、上げる(あげる,調高)⇔下げる(さげる,調低) 都可套用同一種「反義字頭＋共同字尾」記法。
- **通訊資料流口訣**：シリアル(serial,序列傳輸)→パケット(packet,封包)→送信/受信(收發)→ポート(port,埠口)，這是嵌入式通訊的標準資料流動路徑，依序記憶即可還原一次除錯對話。
- **開發流程動詞鏈**：実装(じっそう,implement 寫進程式/硬體)→デバッグ(debug)→シミュレーション(simulation)→書換え(かきかえ,改寫)/リプログラム(reprogram,重新燒錄是嵌入式軟體從開發到部署的標準生命週期，按順序背誦更容易記住每的使用時機。
- **量測操作句型「動詞＋てください」**：時間軸を広げてください(拉寬軸))時間軸を長くしてください(把時間軸調長)是示波器操作中最常用的兩種同義句，"広げる"(拡げる,拉寬展)和"長くする"(調長)可互換使用，職場口語常混用。
- **狀態機三件套**：状態(じょうたい,state)→遷移(せんい,transition)→判定(はんてい,decision/判斷)，畫成ブロック図(ぶろっくず,方塊圖)即為典型的状態機(state machine)描述方式，三詞按邏輯順序記憶。

## ⚠️ 易混淆對比
| 易混組合 | 差異 |
|---|---|
| 機能(きのう) vs 昨日(きのう) | **同音異字！** 機能機能function/功能(軟硬體語境);昨日昨日yesterday(時間語境)，發音完全相同，只能靠上下文判斷，是職場口語常見的聽力陷阱|
| 実装(じっそう) vs 実際(じっさい) | 実装(implement,把功能寫進系統/燒錄體) vs 実際(actual,實際上/事實上)，兩字第二音節發音不同(そう vs さい)。原稿誤將「実装してある」讀作「じっさいしてある」，正確應讀「**じっそうしてある**」(已經實作/已寫入) |
| 制御(せいぎょ) vs コントロール | 兩者同義都是「控制」，制御是和語漢字詞(較正式/書面語，常見於技術文件)，コントロール是外來語(較口語，常見於日常對話)，語境可互換但正式報告偏好用「制御」 |
| 縮小(しゅくしょう) 讀音 | 原稿誤讀「しゅくしょ」(漏音)，正確讀音為「**しゅくしょう**」(長音不可省略)，與「拡大(かくだい)」相對 |
| チャタリング 誤解 | 原稿誤標為「蜂鳴器」，正確意義是**接點抖動／彈跳**(機械開關/繼電器切換瞬間的訊號雜訊)，與蜂鳴器(ブザー)完全無關，是嵌入式硬體除錯常見詞 |
| 以上(いじょう) vs 異常(いじょう) | 同音異字！以上以上"...以上"(數量/等級);異常異常abnormal(狀態異常，故障語境)，發音完全相同，除錯對話中容易聽錯方向(到底是數值上,還是狀態異常) |

## 📡 通訊與資料傳輸

| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| シリアル | シリアル | shiriaru | 序列(通訊) | serial |
| シリアルポート | シリアルポート | shiriaru pooto | 序列埠 | serial port |
| パケット | パケット | paketto | 封包 | packet |
| <ruby>受信<rt>じゅしん</rt></ruby> | じゅしん | jushin | 接收 | receive |
| <ruby>送信<rt>そうしん</rt></ruby> | そうしん | soushin | 發送 | transmit |
| <ruby>送付<rt>そうふ</rt></ruby> | そうふ | soufu | 寄送、送交 | sending |
| ポート | ポート | pooto | 埠口 | port |
| バイナリ | バイナリ | bainari | 二進位 | binary |

## 🛠️ 開發流程

| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| <ruby>実装<rt>じっそう</rt></ruby> | じっそう | jissou | 實作、寫入 | implementation |
| デバッグ | デバッグ | debaggu | 除錯 | debug |
| シミュレーション | シミュレーション | shimyureeshon | 模擬 | simulation |
| パラメータ | パラメータ | parameeta | 參數 | parameter |
| <ruby>書換<rt>かきか</rt></ruby>え | かきかえ | kakikae | 改寫 | rewrite |
| リプログラム | リプログラム | ripuroguramu | 重新燒錄| reprogram |
| <ruby>割付<rt>わりつけ</rt></ruby> | わりつけ | waritsuke | 配置、分配 | allocation/layout |
| エラー | エラー | eraa | 錯誤 | error |
| フィルタ | フィルタ | firuta | 濾波器 | filter |
| リセット | リセット | risetto | 重置 | reset |

## 🔀 狀態機與邏輯

| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| <ruby>状態<rt>じょうたい</rt></ruby> | じょうたい | joutai | 狀態 | state |
| <ruby>遷移<rt>せんい</rt></ruby> | せんい | sen'i | 遷移、轉換 | transition |
| <ruby>判定<rt>はんてい</rt></ruby> | はんてい | hantei | 判定、判斷 | decision |
| ブロック<ruby>図<rt>ず</rt></ruby> | ブロックず | burokku zu | 方塊圖 | block diagram |
| <ruby>機能<rt>きのう</rt></ruby> | きのう | kinou | 功能 | function |

## 📏 量測與示波器

| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| オシロスコープ | オシロスコープ | oshirosukoopu | 示波器 | oscilloscope |
| <ruby>時間軸<rt>じかんじく</rt></ruby> | じかんじく | jikanjiku | 時間軸 | time axis |
| <ruby>縦軸<rt>たてじく</rt></ruby> | たてじく | tatejiku | 縱軸 | vertical axis |
| <ruby>拡大<rt>かくだい</rt></ruby> | かくだい | kakudai | 放大 | zoom in |
| <ruby>縮小<rt>しゅくしょう</rt></ruby> | しゅくしょう | shukushou | 縮小 | zoom out |
| <ruby>検出<rt>けんしゅつ</rt></ruby> | けんしゅつ | kenshutsu | 檢測 | detection |
| <ruby>誤差<rt>ごさ</rt></ruby> | ごさ | gosa | 誤差 | error/deviation |
| バラツキ | バラツキ | baratsuki | 變異、離散度 | variation/scatter |
| <ruby>線形補間<rt>せんけいほかん</rt></ruby> | せんけいほかん | senkei hokan | 線性插值| linear interpolation |
| <ruby>比較<rt>ひかく</rt></ruby> | ひかく | hikaku | 比較 | comparison |

### 實用句
- 「**時間軸を広げてください**」(請把時間軸拉寬／「時間軸を長くしてください」(請把時間軸調長)——示波器除錯時最常用的請求句型，兩者同義可互換。

## ✚ 補充：軟硬體常用詞
| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| ハードウェア | ハードウェア | haadowea | 硬體 | hardware |
| ソフトウェア | ソフトウェア | sofutowea | 軟體 | software |
| センサ | センサ | sensa | 感測器 | sensor |
| シーケンス | シーケンス | shiikensu | 序列、時序 | sequence |
| <ruby>割り込<rt>わりこ</rt></ruby>み | わりこみ | warikomi | 中斷 | interrupt |
| レジスタ | レジスタ | rejisuta | 暫存器 | register |
| ファームウェア | ファームウェア | faamuwea | 韌 | firmware |
| <ruby>外部<rt>がいぶ</rt></ruby> | がいぶ | gaibu | 外部 | external |
| ユニット | ユニット | yunitto | 單元 | unit |
| <ruby>立ち上<rt>たちあ</rt></ruby>がり | たちあがり | tachiagari | 上升緣(訊號) | rising edge |

## 關係說明
- 本卡 [[JP_Work_01_electrical_power|電氣電力 @sibling_of]]、[[JP_Work_03_engineering_actions|工程動作與過程詞 @sibling_of]] 同屬「工作 仕事」職場工程詞彙三部曲，嵌入式軟體詞彙常與電力電子硬體(如馬達驅動狀態機)搭配使用。
- 與 [[JP_Vocab_09_work_school|高頻詞彙 09：工作與學校 @extends]] 中的通用職場詞彙互為延伸，該卡供日常職場用語基礎，本卡入嵌入式開發與量測專業術語。
