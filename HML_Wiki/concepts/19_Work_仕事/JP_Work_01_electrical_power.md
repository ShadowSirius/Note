---
extends:
  - "[[JP_Vocab_09_work_school]]"
sibling_of:
  - "[[JP_Work_02_embedded_software]]"
  - "[[JP_Work_03_engineering_actions]]"
---
# 工程詞彙 01：電氣電力

## 🧠 記憶鉤
- **三電力記法**：有効電力(ゆうこうでんりょく)＝真正「做功」的電力(有効＝有效)；無効電力(むこうでんりょく)＝來回震盪不做功的「虛功」(無効＝無效)；皮相電力(ひそうでんりょく)＝兩者向量和，"皮相"字源即「表面」，意指從外部量測到的「表面上總電力」(視在功率)。三者關係：皮相² = 有効² + 無効²，比值即力率(りきりつ)。
- **〜率家族**：効率(こうりつ,輸出/輸入能量比)、能率(のうりつ,單位時間工作效率)、力率(りきりつ,有效功率/皮相功率)、歪率(ひずみりつ,THD 總諧波失真)——四詞字尾都是「率」，代表某種「比值」，但分母分子各不同，需個別記憶語境：効率談能量轉換、能率談生產力、力率談交流電相位、歪率談波形純度。
- **過〜前綴系**：過電流(かでんりゅう,overcurrent)、過負荷(かふか,overload)、過剰(かじょう,excess/過多)——「過」字頭一律表示「超過正常值」，是電力保護電路故障用語的高頻字首，看到「過」開頭先聯想「超標、要保護跳脫」。
- **送受/収受對稱思維延伸到電力**：交流訊號中「進み電流(すすみでんりゅう,leading)⇔遅れ電流(おくれでんりゅう,lagging)」是一組相位對稱詞，電容性負載電流「進む」(領先電壓)，電感性負載電流「遅れる」(落後電壓)——記口訣「電容超前搶跑,電感落後拖延」。
- **馬達驅動三態**：力行(りきこう,牽引/驅動輸出動力)⇔回生(かいせい,回生煞車/反向發電回充)，是馬達控制的一組相反動作；界磁(かいじ)則是產生磁場的激磁繞組，串聯在馬達控制的「印加(いんか,外加電壓)→界磁→巻き線(まきせん,繞組)」流程中。

## ⚠️ 易混淆對比
| 易混組合 | 差異 |
|---|---|
| 磁界(じかい) vs 界磁(かいじ) | **字序相反、意義完全不同！** 磁界＝magnetic field(磁場本身,物理空間概念);界磁＝field winding(激磁繞組,馬達內部產生磁場的線圈結構)。工程對話中順序讀反會造成理解錯誤,務必逐字確認 |
| 効率(こうりつ) vs 能率(のうりつ) | 効率＝輸出/輸入的能量轉換比(如馬達効率 95%);能率＝單位時間內完成工作量的效率(較偏生產力/作業效率概念),兩者常被誤用為同義詞但語境不同 |
| 力行(りきこう) vs 力率(りきりつ) | 字形相近(都以「力」開頭)但完全不同領域:力行＝馬達/鐵道語境的「驅動運轉」動作;力率＝交流電力學的「功率因數」數值,發音也不同(りきこう vs りきりつ) |
| パワー vs バワー | パワー(pawaa)才是正確外來語「power」;バワー是清濁音誤植(パ→バ),常見手寫筆誤,務必用半濁音「パ」 |
| 力行(りきこう) 讀音查證 | 手稿原標注 りっこう(促音)有疑義；鐵道・馬達控制業界標準讀音為「りきこう」(如惰行だこう、制動せいどう同系詞皆非促音化)，此處以 りきこう 為準 |
| 単相(たんそう) vs 三相(さんそう,補) | 単相＝家用/小型設備的單相交流電;三相則是工業馬達常用的三相交流電,字面「相」數不同即代表電力系統架構不同 |

## 📊 電路基礎與三電力

| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| 直列 | ちょくれつ | chokuretsu | 串聯 | series |
| 並列 | へいれつ | heiretsu | 並聯 | parallel |
| 回路 | かいろ | kairo | 電路、迴路 | circuit |
| 発電 | はつでん | hatsuden | 發電 | power generation |
| 電圧 | でんあつ | den'atsu | 電壓 | voltage |
| 電流 | でんりゅう | denryuu | 電流 | current |
| 交流 | こうりゅう | kouryuu | 交流電 | AC |
| 単相 | たんそう | tansou | 單相 | single-phase |
| インピーダンス | インピーダンス | inpiidansu | 阻抗 | impedance |
| 有効電力 | ゆうこうでんりょく | yuukou denryoku | 有效功率 | active power |
| 無効電力 | むこうでんりょく | mukou denryoku | 無效功率(虛功) | reactive power |
| 皮相電力 | ひそうでんりょく | hisou denryoku | 視在功率 | apparent power |
| 力率 | りきりつ | rikiritsu | 功率因數 | power factor |
| 効率 | こうりつ | kouritsu | 效率 | efficiency |
| 能率 | のうりつ | nouritsu | 工作效率 | work rate |
| パワー | パワー | pawaa | 動力、功率 | power |
| 出力 | しゅつりょく | shutsuryoku | 輸出 | output |
| 入力 | にゅうりょく | nyuuryoku | 輸入 | input |
| 同期発電機 | どうきはつでんき | douki hatsudenki | 同步發電機 | synchronous generator |

## 〰️ 波形與訊號特性

| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| 周波数 | しゅうはすう | shuuhasuu | 頻率 | frequency |
| 高調波 | こうちょうは | kouchouha | 諧波 | harmonics |
| 振幅 | しんぷく | shinpuku | 振幅 | amplitude |
| 位相 | いそう | isou | 相位 | phase |
| 進み電流 | すすみでんりゅう | susumi denryuu | 超前電流 | leading current |
| 遅れ電流 | おくれでんりゅう | okure denryuu | 滯後電流 | lagging current |
| 歪率 | ひずみりつ | hizumiritsu | 總諧波失真率 | THD |
| ずれ | ずれ | zure | 偏差、偏移 | deviation |
| 安定 | あんてい | antei | 穩定 | stability |
| ゼロクロス | ゼロクロス | zerokurosu | 過零點 | zero-crossing |

## ⚙️ 馬達驅動與保護

| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| 力行 | りきこう | rikikou | 驅動運轉(牽引) | powering/traction |
| 回生 | かいせい | kaisei | 回生煞車 | regenerative braking |
| モーター | モーター | mootaa | 馬達 | motor |
| 制御 | せいぎょ | seigyo | 控制 | control |
| 抑制 | よくせい | yokusei | 抑制 | suppression |
| 印加 | いんか | inka | 外加電壓 | applied voltage |
| 定格 | ていかく | teikaku | 額定 | rated value |
| 磁石 | じしゃく | jishaku | 磁鐵 | magnet |
| 磁界 | じかい | jikai | 磁場 | magnetic field |
| 界磁 | かいじ | kaiji | 激磁繞組 | field winding |
| 巻き線 | まきせん | makisen | 繞組、線圈 | winding |
| 過電流 | かでんりゅう | kadenryuu | 過電流 | overcurrent |
| 過負荷 | かふか | kafuka | 過負載 | overload |
| サージ | サージ | saaji | 突波 | surge |

## ✚ 補充：元件與周邊詞彙
| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| コンデンサ | コンデンサ | kondensa | 電容 | capacitor |
| コイル | コイル | koiru | 線圈 | coil |
| チョーク | チョーク | chooku | 扼流圈(電感) | choke |
| 素子 | そし | soshi | 元件 | (circuit) element |
| ゲート | ゲート | geeto | 閘極 | gate |
| カプラ | カプラ | kapura | 耦合器 | coupler |
| ハーネス | ハーネス | haanesu | 線束 | wiring harness |
| エミッション | エミッション | emisshon | 電磁干擾發射 | EMI emission |
| チャタリング | チャタリング | chatearingu | 接點抖動／彈跳(原稿誤標「蜂鳴器」) | contact chattering/bounce |
| 半田吸い取り器 | はんだすいとりき | handa suitoriki | 吸錫器 | solder sucker |
| 整流 | せいりゅう | seiryuu | 整流 | rectification |
| インバータ | インバータ | inbaata | 變頻器/逆變器 | inverter |
| 絶縁 | ぜつえん | zetsuen | 絕緣 | insulation |
| 接地 | せっち | secchi | 接地 | grounding |
| 短絡 | たんらく | tanraku | 短路 | short circuit |

## 關係說明
- 本卡與 [[JP_Work_02_embedded_software|嵌入式與軟體 @sibling_of]]、[[JP_Work_03_engineering_actions|工程動作與過程詞 @sibling_of]] 同屬「工作 仕事」職場工程詞彙三部曲，共同構成電力電子/馬達控制工程師的專業日語底層。
- 與 [[JP_Vocab_09_work_school|高頻詞彙 09：工作與學校 @extends]] 中的日常職場詞彙互為延伸，該卡提供通用職場用語，本卡深入電力電子專業術語。
