# 같은 사건, 다른 제목 — 뉴스 헤드라인 프레이밍 분석

서강대 ENG3510 「인공지능을 위한 데이터분석」 팀 프로젝트입니다. 같은 사건을 언론사마다 어떤 관점(프레임)으로 제목을 붙이는지 비교하고, Claude가 붙인 프레임이 사람의 판단과 얼마나 일치하는지 검증합니다.

현재 단계: **1주치 파일럿 완료, 라벨링 기준(v3) 확정 → 팀원 라벨링 준비 중** (2026-11-13 기준)

## 탐구 질문

1. 같은 사건의 헤드라인에서 언론사별 프레임 선택은 얼마나 갈리는가?
2. 프레임은 어떤 표현(주체, 동사, 수치, 인용)으로 드러나는가?
3. Claude가 붙인 프레임은 사람이 붙인 것과 얼마나 일치하는가?

특정 언론사가 편향됐다는 결론이 아니라, 프레임 분포를 기술하는 것이 목표입니다.

## 지금까지 한 일

| 단계 | 내용 |
| --- | --- |
| 1. 데이터 수집 | 빅카인즈에서 2026-10-28 ~ 11-04 기사 16,058건 (주요 언론사 12곳, 통합분류 정치·경제·사회). 전체 언론사로 받으면 1회 다운로드 한도(2만 건)에 걸려 사흘치만 들어와서 12곳으로 줄였음 |
| 2. 사건 묶기 | 제목·키워드 유사도로 기사를 묶고, 10곳 이상이 다룬 사건 중 분야가 겹치지 않게 16개 선정 → 헤드라인 515건. 사진 설명 제목, 개인 피해자 중심 범죄 사건은 제외. 주가처럼 날마다 바뀌는 지표는 날짜별로 분리 |
| 3. 코드북 | 프레임 7개 정의 ([docs/codebook.md](docs/codebook.md)) |
| 4. 1차 분류 (v1) | Claude가 515건에 프레임을 하나씩 붙임. 겹치면 고정 우선순위로 선택 |
| 5. 기준 개정 (v2 → v3) | 우선순위 대신 "기본 사실을 빼고 남는 표현"으로 판단, 대등할 때만 서브 프레임 추가, 대책 발표 사건 규칙 추가 |
| 6. 스킬 | 라벨링 절차를 Claude 스킬로 만듦 ([skills/headline-frame-labeling](skills/headline-frame-labeling/SKILL.md)) |
| 7. 스킬 테스트 | 3개 사건 59건으로 v1과 v3 비교 ([pages/frame_compare.html](pages/frame_compare.html)) |

### 언론사 12곳

- 종합일간지: 조선일보, 중앙일보, 동아일보, 한국일보, 경향신문, 한겨레
- 경제지: 매일경제, 한국경제
- 방송: KBS, MBC, SBS, YTN

## 프레임 7개 (요약)

| 프레임 | 정의 | 출처 |
| --- | --- | --- |
| 사실 전달 | 기본 사실 말고 남는 표현이 없음 | 자체 범주 |
| 갈등 | 행위자 간 대립과 반발 | Semetko & Valkenburg (2000) |
| 원인·책임 | 이유나 책임 주체를 밝힘 | Semetko & Valkenburg (2000), Entman (1993) |
| 부정 결과·우려 | 손실, 위험, 대가, 고통 | Semetko & Valkenburg (2000) |
| 긍정 성과 | 기록, 회복, 혜택 | Semetko & Valkenburg (2000) |
| 대응·조치 | 문제를 막거나 수습하려는 대책 | Entman (1993) |
| 기타 | 판단 불가 (사설의 당부 등) | 자체 범주 |

판단 절차와 예시는 [docs/codebook.md](docs/codebook.md)에 있습니다.

## 결과

### 파일럿 (v1 기준, 515건)

- 전체: 사실 전달 240, 갈등 68, 부정 68, 긍정 56, 원인·책임 48, 대응·조치 32, 기타 3
- 프레임은 언론사 유형보다 **사건에 따라** 크게 달라졌음
- 진성준 비자 논란: 53건 중 갈등 23건 (여야 공방 인용)
- 윤석열 선거법 2심: 42건 중 34건이 판결보다 "국힘 397억 반환"을 앞세움
- 10월 소비자물가: 같은 2.8%를 "두 달 연속 둔화"(긍정)와 "석유류 뜀박질"(부정)로 보도

### 기준 개정 테스트 (v1 vs v3, 59건)

| 사건 | 바뀐 건수 | 주요 변화 |
| --- | --- | --- |
| 10월 소비자물가 | 0 / 17 | 변화 없음 |
| 아주대 소아응급 집단사직 | 5 / 21 | 따옴표로 강조된 "손 떨려"가 메인이 되며 원인·책임 10 → 5, 부정 7 → 11 |
| 수능 AI 안경 처벌 | 1 / 21 | "주의보" 1건만 부정으로 바뀌고 대응·조치는 서브로 남음 |

- 메인 일치 53/59 (90%), 서브가 붙은 제목 4건 (7%)
- v1 기준만 쓰면 아주대 사건의 결론이 "원인 중심"에서 "호소 중심"으로 뒤집힐 수 있어서, **분류 규칙이 결론에 영향을 준다**는 점을 확인함
- 두 라벨 모두 Claude가 붙인 것이므로 정확도가 아니라 기준 변경의 영향을 본 결과임

## 폴더 구조

```
data/
  pilot/headlines.csv            파일럿 헤드라인 515건 (스킬 입력 형식)
  pilot/headlines_week_v1.csv    515건 + v1 프레임 라벨
  skill-test/                    스킬 테스트 입력·출력 (59건, 기본 사실, v1과 다른 제목)
docs/codebook.md                 코드북과 판단 규칙 (v3)
pages/frame_compare.html         v1 vs v3 비교 페이지 (브라우저로 열기)
pages/pilot_dashboard_source.html 파일럿 대시보드 페이지 소스 (Claude 대시보드용)
scripts/cluster.py               제목·키워드 유사도로 사건 묶기
scripts/pick12.py                사건 선정과 키워드 추출
scripts/label12.py               v1 라벨 적용과 집계
skills/headline-frame-labeling/  프레임 라벨링 Claude 스킬 (v3)
```

빅카인즈 원본 엑셀은 용량(18.6MB)과 이용약관 확인 전이라 올리지 않았습니다.

## 다음 할 일

- [ ] 팀원별 독립 라벨링 (v3 코드북 기준)
- [ ] 일치도 계산 (Krippendorff's α, Cohen's κ): 사람끼리, 사람 vs v1, 사람 vs v3
- [ ] 인간적 흥미 프레임 추가 여부 결정 ("손 떨려 진료 못 해" 같은 호소)
- [ ] 기간을 늘려 사건 30–40개, 약 2,000건으로 확대
- [ ] 빅카인즈 이용약관의 결과 공개 범위 확인
- [ ] TF-IDF + 로지스틱 회귀 기준 모델
- [ ] (선택) 크롬 확장 프로그램 데모

## 참고 문헌

- Semetko, H. A., & Valkenburg, P. M. (2000). [Framing European politics: A content analysis of press and television news](https://doi.org/10.1111/j.1460-2466.2000.tb02843.x). *Journal of Communication*, 50(2).
- Entman, R. M. (1993). [Framing: Toward clarification of a fractured paradigm](https://doi.org/10.1111/j.1460-2466.1993.tb01304.x). *Journal of Communication*, 43(4).
- Liu, S. et al. (2019). [Detecting Frames in News Headlines and Its Application to Analyzing News Framing Trends Surrounding U.S. Gun Violence](https://aclanthology.org/K19-1047/). CoNLL.
- Card, D. et al. (2015). [The Media Frames Corpus](https://aclanthology.org/P15-2072/). ACL.
