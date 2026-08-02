---
extends:
  - "[[JP_Vocab_09_work_school]]"
sibling_of:
  - "[[JP_Work_02_embedded_software]]"
  - "[[JP_Work_03_engineering_actions]]"
---
# 工程詞彙 01：電氣電力

## 🧠 記憶鉤
- **三電力記法**：有効電力(ゆうこうでんりょく))真正「做功」的電力(有効有効有效))無効電力(むこうでんりょく))來回震盪不做功的「虛(無効無効無效))皮相電力(ひそうでんりょく))兩者向量和，"皮相"字源即「表面」，意指從外部量測到的「表面上總電力」(視在功率)。三者關係：皮相² = 有効² + 無効²，比值率(りきりつ)。
- **〜率家族**：効率(こうりつ,輸出/輸入能量比)、能率(のうりつ,單位時間工作效率)、力率(りきりつ,有效功率/皮相功率)、歪率(ひずみりつ,THD 總諧波失真)——四詞字尾都是「率」，代表某種「比值但分母分子各不同，需個別記憶語境：効率談能量轉換、能率談生產力率談交流電相位、歪率談波形純度。
- **過〜前綴系**：過電流(かでんりゅう,overcurrent)、過負荷(かふか,overload)、過剰(かじょう,excess/過多)——「過」字頭一律表示「超過正常值是電力保護電路故障用語的高頻字首，看到「過」開頭先聯想「超標、要保護跳脫
- **送受/収受對稱思維延伸到電力**：交流訊號中「進み電流(すすみでんりゅう,leading)⇔遅れ電流(おくれでんりゅう,lagging)」是一組相位對稱詞，電容性負載電流「進む」(領先電壓)，電感性負載電流「遅れる」(落後電壓)——記口訣「電容超前搶跑感落後拖。
- **馬達驅動三態**：力行(りきこう,牽引/驅動輸出動力)⇔回生(かいせい,回生煞反向發電回充)，是馬達控制的一組相反動作動作界磁(かいじ)則是產場的激磁繞組，串聯在馬達控制的「印加(いんか,外加電壓)→界磁→巻き線(まきせん,繞組)」流程中。

## ⚠️ 易混淆對比
| 易混組合 | 差異 |
|---|---|
| 磁界(じかい) vs 界磁(かいじ) | **字序相反、意義完全不同！** 磁界磁界magnetic field(磁場本身,物理空間概念);界磁磁field winding(激磁繞組,馬達內產磁場的線圈結構)。工程對話中順序讀反會造成理解錯誤,務必逐字確認 |
| 効率(こうりつ) vs 能率(のうりつ) | 効率効率輸出/輸入的能量轉換比(如馬達効率 95%);能率能率單位時間內成工作量的效率(較偏生產/作業效率概念),兩者常被誤用為同義詞但語境不同 |
| 力行(りきこう) vs 力率(りきりつ) | 字形相近(都以「力」開頭)但完全不同領域:力行力行馬達/鐵道語境的「驅動運轉」動作;力率力率交流電力學的「功率因數」數值音也不同(りきこう vs りきりつ) |
| パワー vs バワー | パワー(pawaa)才是正確外來語「power」;バワー是清濁音誤植(パ→バ),常見手寫筆誤,務必用半濁音「パ」 |
| 力行(りきこう) 讀音查| 手稿原標注 りっこう(促音)有疑義疑義鐵道・馬達控制業界標準讀音為「りきこう」(如惰行だこう、制動せいどう同系詞皆非促音化)，此處以 りきこう 為準 |
| 単相(たんそう) vs 三相(さんそう,補) | 単相単相家用/小型設備的單相交流電;三相則是工業馬達常用的三相交流電,字面「相」數不同即代表電力系統架構不同 |

## 📊 電路基礎與三電力

| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| <ruby>直列<rt>ちょくれつ</rt></ruby> | ちょくれつ | chokuretsu | 串聯 | series |
| <ruby>並列<rt>へいれつ</rt></ruby> | へいれつ | heiretsu | 並聯 | parallel |
| <ruby>回路<rt>かいろ</rt></ruby> | かいろ | kairo | 電路、迴路 | circuit |
| <ruby>発電<rt>はつでん</rt></ruby> | はつでん | hatsuden | 發電 | power generation |
| <ruby>電圧<rt>でんあつ</rt></ruby> | でんあつ | den'atsu | 電壓 | voltage |
| <ruby>電流<rt>でんりゅう</rt></ruby> | でんりゅう | denryuu | 電流 | current |
| <ruby>交流<rt>こうりゅう</rt></ruby> | こうりゅう | kouryuu | 交流電 | AC |
| <ruby>単相<rt>たんそう</rt></ruby> | たんそう | tansou | 單相 | single-phase |
| インピーダンス | インピーダンス | inpiidansu | 阻抗 | impedance |
| <ruby>有効<rt>ゆうこう</rt></ruby><ruby>電力<rt>でんりょく</rt></ruby> | ゆうこうでんりょく | yuukou denryoku | 有效功率 | active power |
| <ruby>無効電力<rt>むこうでんりょく</rt></ruby> | むこうでんりょく | mukou denryoku | 無效功率(虛) | reactive power |
| <ruby>皮相<rt>ひそう</rt></ruby><ruby>電力<rt>でんりょく</rt></ruby> | ひそうでんりょく | hisou denryoku | 視在功率 | apparent power |
| <ruby>力率<rt>りきりつ</rt></ruby> | りきりつ | rikiritsu | 功率因數 | power factor |
| <ruby>効率<rt>こうりつ</rt></ruby> | こうりつ | kouritsu | 效率 | efficiency |
| <ruby>能率<rt>のうりつ</rt></ruby> | のうりつ | nouritsu | 工作效率 | work rate |
| パワー | パワー | pawaa | 動力、功率 | power |
| <ruby>出力<rt>しゅつりょく</rt></ruby> | しゅつりょく | shutsuryoku | 輸出 | output |
| <ruby>入力<rt>にゅうりょく</rt></ruby> | にゅうりょく | nyuuryoku | 輸入 | input |
| <ruby>同期<rt>どうき</rt></ruby><ruby>発電機<rt>はつでんき</rt></ruby> | どうきはつでんき | douki hatsudenki | 同步電機 | synchronous generator |

## 〰️ 波形與訊號特性

| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| <ruby>周波数<rt>しゅうはすう</rt></ruby> | しゅうはすう | shuuhasuu | 頻率 | frequency |
| <ruby>高調波<rt>こうちょうは</rt></ruby> | こうちょうは | kouchouha | 諧波 | harmonics |
| <ruby>振幅<rt>しんぷく</rt></ruby> | しんぷく | shinpuku | 振幅 | amplitude |
| <ruby>位相<rt>いそう</rt></ruby> | いそう | isou | 相位 | phase |
| <ruby>進<rt>すす</rt></ruby>み<ruby>電流<rt>でんりゅう</rt></ruby> | すすみでんりゅう | susumi denryuu | 超前電流 | leading current |
| <ruby>遅<rt>おく</rt></ruby>れ<ruby>電流<rt>でんりゅう</rt></ruby> | おくれでんりゅう | okure denryuu | 滯後電流 | lagging current |
| <ruby>歪率<rt>ひずみりつ</rt></ruby> | ひずみりつ | hizumiritsu | 總諧波失真率 | THD |
| ずれ | ずれ | zure | 偏差、偏移 | deviation |
| <ruby>安定<rt>あんてい</rt></ruby> | あんてい | antei | 穩定 | stability |
| ゼロクロス | ゼロクロス | zerokurosu | 過零點 | zero-crossing |

## ⚙️ 馬達驅動與保護

| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| <ruby>力行<rt>りっこう</rt></ruby> | りきこう | rikikou | 驅動運轉(牽引) | powering/traction |
| <ruby>回生<rt>かいせい</rt></ruby> | かいせい | kaisei | 回生煞 | regenerative braking |
| モーター | モーター | mootaa | 馬達 | motor |
| <ruby>制御<rt>せいぎょ</rt></ruby> | せいぎょ | seigyo | 控制 | control |
| <ruby>抑制<rt>よくせい</rt></ruby> | よくせい | yokusei | 抑制 | suppression |
| <ruby>印加<rt>いんか</rt></ruby> | いんか | inka | 外加電壓 | applied voltage |
| <ruby>定格<rt>ていかく</rt></ruby> | ていかく | teikaku | 額定 | rated value |
| <ruby>磁石<rt>じしゃく</rt></ruby> | じしゃく | jishaku | 磁鐵 | magnet |
| <ruby>磁界<rt>じかい</rt></ruby> | じかい | jikai | 磁場 | magnetic field |
| <ruby>界<rt>かい</rt></ruby><ruby>磁<rt>じ</rt></ruby> | かいじ | kaiji | 激磁繞組 | field winding |
| <ruby>巻き線<rt>まきせん</rt></ruby> | まきせん | makisen | 繞組、線圈 | winding |
| <ruby>過<rt>か</rt></ruby><ruby>電流<rt>でんりゅう</rt></ruby> | かでんりゅう | kadenryuu | 過電流 | overcurrent |
| <ruby>過負荷<rt>かふか</rt></ruby> | かふか | kafuka | 過負載 | overload |
| サージ | サージ | saaji | 突波 | surge |

## ✚ 補充：元件與周邊詞彙
| 日文 | 假名 | 羅馬字 | 中文 | 英文 |
|---|---|---|---|---|
| コンデンサ | コンデンサ | kondensa | 電容 | capacitor |
| コイル | コイル | koiru | 線圈 | coil |
| チョーク | チョーク | chooku | 扼流圈(電感) | choke |
| <ruby>素子<rt>もとこ</rt></ruby> | そし | soshi | 元件 | (circuit) element |
| ゲート | ゲート | geeto | 閘極 | gate |
| カプラ | カプラ | kapura | 耦器 | coupler |
| ハーネス | ハーネス | haanesu | 線束 | wiring harness |
| エミッション | エミッション | emisshon | 電磁干擾發射 | EMI emission |
| チャタリング | チャタリング | chatearingu | 接點抖動／彈跳(原稿誤標「蜂鳴器」) | contact chattering/bounce |
| <ruby>半田<rt>はんだ</rt></ruby><ruby>吸<rt>す</rt></ruby>い<ruby>取<rt>と</rt></ruby>り<ruby>器<rt>うつわ</rt></ruby> | はんだすいとりき | handa suitoriki | 吸錫器 | solder sucker |
| <ruby>整流<rt>せいりゅう</rt></ruby> | せいりゅう | seiryuu | 整流 | rectification |
| インバータ | インバータ | inbaata | 變頻器/逆變器 | inverter |
| <ruby>絶縁<rt>ぜつえん</rt></ruby> | ぜつえん | zetsuen | 絕 | insulation |
| <ruby>接地<rt>せっち</rt></ruby> | せっち | secchi | 接地 | grounding |
| <ruby>短絡<rt>たんらく</rt></ruby> | たんらく | tanraku | 短路 | short circuit |

## 關係說明
- 本卡 [[JP_Work_02_embedded_software|嵌入式與軟體 @sibling_of]]、[[JP_Work_03_engineering_actions|工程動作與過程詞 @sibling_of]] 同屬「工作 仕事」職場工程詞彙三部曲，共同構成電力電子/馬達控制工程師的專業日語底層。
- 與 [[JP_Vocab_09_work_school|高頻詞彙 09：工作與學校 @extends]] 中的日常職場詞彙互為延伸，該卡供通用職場用語，本卡入電力電子專業術語。
