# 🇯🇵 日語動詞分類與九大語形變化指南

> [!important] 句子結構色彩標記：
> >  **主語/主題** (`#2ECC71`) \|  \|  **核心/謂語** (`#3498DB`) \|  \|  **修飾語/賓語** (`#E67E22`) \|  \|  **時間/場所/副詞** (`#E74C3C`)

---

## 📂 第一部分：動詞分類判斷

日語動詞依其字尾及變形規律分為三大類。快速判定方法如下：

```mermaid
graph TD
    A["動詞原形 (最後一個字為 u 段音)"] --> B{"是否為 する 或 くる (来る)？"}
    B -- 是 --> C["III 類動詞 (不規則變形)"]
    B -- 否 --> D{"字尾是否為 る (ru)？"}
    D -- 否 --> E["I 類動詞 (五段動詞)"]
    D -- 是 --> F{"る 前一個字是否為 i 或 e 段音？"}
    F -- 否 --> E
    F -- 是 --> G["II 類動詞 (一段動詞)"]
    
    style C fill:#e74c3c,stroke:#333,stroke-width:2px;
    style E fill:#3498db,stroke:#333,stroke-width:2px;
    style G fill:#2ecc71,stroke:#333,stroke-width:2px;
```

> [!warning] I 類動詞（五段動詞）的特例（る前為 i/e 段音卻屬於 I 類）：
> - **帰る（かえる / 回家）**、**入る（はいる / 進入）**、**走る（はしる / 奔跑*、**知る（しる / 知道）**、**切る（きる / 剪切）**。

---

## 📂 第二部分：動詞九大基本變形規則與例句對照

| 變形種類 | I 類動詞 (以「書く」/「買う」為例) | II 類動詞 (以「食べる」為例) | III 類動詞 (以「する」/「来る」為例) | 語境與結構例句 |
| :--- | :--- | :--- | :--- | :--- |
| **① 辭書形** <br>(原形/字典形) | 字尾以 **u段音** 結尾。 <br> 例：`書く` (kaku) / `買う` (kau) | 去掉字尾 **る**。 <br> 例：`食べる` (taberu) | `する` (suru / 做) <br> `来る` (kuru / 來) | <span style="color:#2ECC71"><ruby>私<rt>わたし</rt></ruby>は</span><span style="color:#E67E22"><ruby>本<rt>ほん</rt></ruby>を</span><span style="color:#3498DB"><ruby>書<rt>か</rt></ruby>く。</span> <br>（<ruby>我<rt>われ</rt></ruby><ruby>寫書<rt>しゃしょ</rt></ruby>。） |
| **② ます形** <br>(丁寧形/禮貌) | 字尾 **u段** 變為 **i段** + `ます`。 <br> 例：`書きます` / `買います` | 去掉 **る** + `ます`。 <br> 例：`食べます` | `します` (shimasu) <br> `来ます` (kimasu) | <span style="color:#2ECC71"><ruby>先生<rt>せんせい</rt></ruby>は</span><span style="color:#E74C3C"><ruby>明日<rt>あした</rt></ruby></span><span style="color:#3498DB"><ruby>来<rt>き</rt></ruby>ます。</span> <br>（<ruby>老師<rt>ろうし</rt></ruby><ruby>明<rt>めい</rt></ruby><ruby>天會<rt>てんかい</rt></ruby><ruby>來<rt>らい</rt></ruby>。） |
| **③ て形** <br>(連接/進行) | **促音便** (う/つ/る → って) <br>**鼻音便** (ぬ/ぶ/む → んで) <br>**い音便** (く → いて / ぐ → いで) <br> 例：`書いて` / `買って` | 去掉 **る** + `て`。 <br> 例：`食べて` | `して` (shite) <br> `来て` (kite) | <span style="color:#E67E22">リンゴを</span><span style="color:#3498DB"><ruby>食<rt>た</rt></ruby>べてください。</span> <br>（<ruby>請<rt>せい</rt></ruby><ruby>吃<rt>きつ</rt></ruby><ruby>蘋果<rt>ひんか</rt></ruby>。） |
| **④ た形** <br>(過去式/完成) | 變形規律與 **て形** 完全一致，`て` 變 `た`，`為` 變 `だ`。 <br> 例：`書いた` / `買った` | 去掉 **る** + `た`。 <br> 例：`食べた` | `した` (shita) <br> `来た` (kita) | <span style="color:#E74C3C"><ruby>昨日<rt>きのう</rt></ruby>、</span><span style="color:#2ECC71"><ruby>彼<rt>かれ</rt></ruby>が</span><span style="color:#3498DB"><ruby>来<rt>き</rt></ruby>た。</span> <br>（<ruby>昨<rt>さく</rt></ruby><ruby>天<rt>てん</rt></ruby><ruby>他<rt>ほか</rt></ruby><ruby>來<rt>らい</rt></ruby><ruby>了<rt>りょう</rt></ruby>。） |
| **⑤ ない形** <br>(否定/未然) | 字尾 **u段** 變為 **a段** + `ない` (う結尾變わ)。 <br> 例：`書かない` / `買わない` | 去掉 **る** + `ない`。 <br> 例：`食べない` | `しない` (shinai) <br> `来ない` (konai / 讀作 konai) | <span style="color:#2ECC71"><ruby>私<rt>わたし</rt></ruby>は</span><span style="color:#E67E22"><ruby>肉<rt>にく</rt></ruby>を</span><span style="color:#3498DB"><ruby>食<rt>た</rt></ruby>べない。</span> <br>（<ruby>我<rt>われ</rt></ruby><ruby>不<rt>ふ</rt></ruby><ruby>吃<rt>きつ</rt></ruby><ruby>肉<rt>にく</rt></ruby>。） |
| **⑥ 可能形** <br>(能力/許可) | 字尾 **u段** 變為 **e段** + `る`。 <br> 例：`書ける` / `買える` | 去掉 **る** + `られる` (口語常簡略為 `れる`)。 <br> 例：`食べられる` | `できる` (dekiru) <br> `来られる` (koraredu / 讀作 koraredu) | <span style="color:#2ECC71">日本語が</span><span style="color:#3498DB">話せる。</span> <br>（我會說文。） |
| **⑦ 意向形** <br>(意志/勸誘) | 字尾 **u段** 變為 **o段** + `う`。 <br> 例：`書こう` / `買おう` | 去掉 **る** + `よう`。 <br> 例：`食べよう` | `しよう` (shiyou) <br> `来よう` (koyou / 讀作 koyou) | <span style="color:#E74C3C"><ruby>一緒<rt>いっしょ</rt></ruby>に</span><span style="color:#E67E22"><ruby>映画<rt>えいが</rt></ruby>を</span><span style="color:#3498DB"><ruby>見<rt>み</rt></ruby>よう。</span> <br>（<ruby>一起<rt>かずき</rt></ruby><ruby>看<rt>かん</rt></ruby><ruby>電影<rt>でんえい</rt></ruby><ruby>吧<rt></rt></ruby>|
| **⑧ 受身形** <br>(被動形) | 字尾 **u段** 變為 **a段** + `れる`。 <br> 例：`書かれる` / `買われる` | 去掉 **る** + `られる`。 <br> 例：`食べられる` | `される` (saredu) <br> `来られる` (koraredu) | <span style="color:#2ECC71"><ruby>私<rt>わたし</rt></ruby>は</span><span style="color:#2ECC71"><ruby>犬<rt>いぬ</rt></ruby>に</span><span style="color:#3498DB"><ruby>噛<rt>か</rt></ruby>まれた。</span> <br>（<ruby>我<rt>われ</rt></ruby><ruby>被<rt>ひ</rt></ruby><ruby>狗<rt>く</rt></ruby><ruby>咬<rt>こう</rt></ruby><ruby>了<rt>りょう</rt></ruby>。） |
| **⑨ 使役形** <br>(讓/叫/使) | 字尾 **u段** 變為 **a段** + `せる`。 <br> 例：`書かせる` / `買わせる` | 去掉 **る** + `させる`。 <br> 例：`食べさせる` | `させる` (saseru) <br> `来させる` (kosaseru / 讀作 kosaseru) | <span style="color:#2ECC71"><ruby>母<rt>はは</rt></ruby>は</span><span style="color:#2ECC71"><ruby>子供<rt>こども</rt></ruby>に</span><span style="color:#E67E22"><ruby>勉強<rt>べんきょう</rt></ruby>を</span><span style="color:#3498DB">させる。</span> <br>（<ruby>母親<rt>ははおや</rt></ruby><ruby>讓<rt>ゆずる</rt></ruby><ruby>孩子<rt>がいし</rt></ruby><ruby>學習<rt>がくしゅう</rt></ruby>。） |

---

## 📂 第三部分：て形音便與特殊規則

### 1. 五段動詞「て形 / た形」音便口訣
五段動詞的「て形」與「た形」變化會根據字尾產便：
*   **字尾為「う、つ、る」**：變為 **促音便** `って` / `った`
    *   例：買う → 買って、待つ → 待って、取る → 取って
*   **字尾為「む、ぶ、ぬ」**：變為 **鼻音便** `んで` / `んだ`
    *   例：読む → 読んで、遊ぶ → 遊んで、死ぬ → 死んで
*   **字尾為「く」**：變為 **い音便** `いて` / `いた`
    *   例：書く → 書いて
*   **字尾為「ぐ」**：變為 **い音便（帶濁音）** `いで` / `いだ`
    *   例：泳ぐ → 泳いで
*   **字尾為「す」**：變為 `して` / `した`
    *   例：話す → 話して

> [!important] 唯一特例
> **行く（いく / 去）** 的字尾雖然是「く」，但其て形為促音便的 **行って（いって）**，請特別注意。

---

## 🔗 相關文法卡片連結
動詞的各種形變是學習日語句型的基礎，請參考以下關聯文法卡：
*   **て形應用**：
    *   [[JP_Grammar_11_te_kudasai|〜てください (請做某事)]]
    *   [[JP_Grammar_12_te_imasu|〜ています (正在進行/狀態)]]
    *   [[JP_Grammar_13_te_mo_ii_desu|〜てもいいです (可以做某事)]]
    *   [[JP_Grammar_14_te_wa_ikemasen|〜てはいけません (不准做某事)]]
*   **ない形應用**：
    *   [[JP_Grammar_20_nai_de_kudasai|〜ないでください (請不要做某事)]]
    *   [[JP_Grammar_21_nakereba_narimasen|〜なければなりません (必須做某事)]]
    *   [[JP_Grammar_22_nakute_mo_ii_desu|〜なくてもいいです (不用做某事)]]
*   **た形應用**：
    *   [[JP_Grammar_17_tari_tari_shimasu|〜たり〜たりします (動作並列)]]
    *   [[JP_Grammar_18_ta_koto_ga_arimasu|〜たことがあります (曾經做過)]]
    *   [[JP_Grammar_19_ta_hou_ga_ii_desu|〜たほうがいいです (做某事比較好)]]
*   **其他重要形變**：
    *   [[JP_Grammar_15_tai_desu|〜たいです (想做某事 - 變化規律同い形容詞)]]
    *   [[JP_Grammar_23_koto_ga_dekimasu|〜ことができます (能夠做某事 - 接動詞原形)]]
    *   [[JP_Grammar_24_tsumori_desu|〜つもりです (打算做某事 - 接動詞原形)]]
