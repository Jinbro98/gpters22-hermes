---
name: hermes-md-wizard
description: "Use when the user wants to set up their Hermes agent's identity or work rules — creating a SOUL.md (the agent's persona, tone, and behavior rules — who it is) and/or a HERMES.md (the agent/profile's detailed work rules, like CLAUDE.md — how this agent works). Clearly separates the two files' roles, offers a guided conversational onboarding with examples, ready-made presets, an edit mode, and beginner-friendly explanations. Assembles, backs up, and saves both files to the correct locations automatically."
version: 3.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, soul, SOUL.md, HERMES.md, setup, configuration, onboarding, wizard, persona, agent-rules, beginner]
    related_skills: [hermes-agent, create-hermes-profile]
---

# SOUL.md & HERMES.md 작성 마법사

## Overview

Hermes 에이전트를 설정하는 핵심 파일은 두 가지입니다. 이 둘은 **역할이 완전히 다릅니다.**

- **SOUL.md** — 에이전트가 **누구인가**. 페르소나, 말투, 행동/성격 규칙. 에이전트의 정체성.
- **HERMES.md** — 이 에이전트가 **어떻게 일하는가**. `CLAUDE.md`처럼 상세한 작업 규칙·컨벤션. 이 **에이전트(프로필) 단위**로 적용되는 작업 규칙.

> 🔑 한 줄 기준: **"에이전트가 누구인지(성격)면 SOUL.md, 에이전트가 어떻게 일하는지(작업 규칙)면 HERMES.md."**
> SOUL.md = *누구인지(who)*, HERMES.md = *어떻게 일하는지(how)*. 둘 다 이 에이전트(프로필)에 속합니다.

이 스킬은 **Hermes 입문자**와 **일반 사용자** 모두를 위해 설계됐습니다. 시작할 때 어떤 파일을 만들지(SOUL만 / HERMES만 / 둘 다) 고르고, 친절한 질문에 답하면 두 파일을 알맞은 위치에 만들어 줍니다.

## Bundled Resources

상세 내용은 본문에 다 펼치지 않고 필요할 때 아래 파일을 읽어 사용합니다.

| 파일 | 언제 읽나 |
|---|---|
| `reference/soul-questions.md` | SOUL.md 질문(간단히 S1–S7 / 자세히 S8–S15)을 던질 때 |
| `reference/hermes-questions.md` | HERMES.md 질문(간단히 H1–H5 / 자세히 H6–H10)을 던질 때 |
| `reference/presets.md` | 사용자가 "프리셋" 모드를 고를 때 (SOUL 5종 / HERMES 4종) |
| `reference/templates.md` | 답변을 완성본으로 조립할 때 |
| `examples/SOUL.example.md`, `examples/HERMES.example.md` | 완성 샘플을 보여주거나 품질 기준으로 삼을 때 |
| `scripts/save_hermes_md.py` | 백업·저장을 결정적으로 처리할 때 (Save Flow 참조) |

## The Two Files — 역할 구분 (가장 중요)

| 항목 | **SOUL.md** | **HERMES.md** (= `.hermes.md`) |
|---|---|---|
| **본질** | 에이전트의 정체성·인격 | 에이전트(프로필)의 작업 지침 (최상위 우선순위) |
| **답하는 질문** | 누구인가 (who) | 어떻게 일하는가 (how) |
| **내용** | 이름, 페르소나, 말투, 커뮤니케이션 스타일, 직설성, 스타일상 피할 것, 불확실·이견·모호함 대처 | 에이전트의 작업 방식, 컨벤션, 작업 규칙, 자주 쓰는 명령, 완료 기준 |
| **비유** | 사람의 "성격·말투" | `CLAUDE.md`처럼 에이전트가 따르는 "업무 매뉴얼" |
| **저장 위치** | 루트 폴더의 `SOUL.md` | **같은 루트 폴더**의 `HERMES.md` |
| **루트 폴더** | `~/.hermes/profiles/{프로필}/`이 있으면 그 프로필 폴더, 없으면 `~/.hermes/` | ← 두 파일 모두 **동일한** 루트에 함께 둠 |
| **우선순위** | 정체성으로 독립 로드 | `HERMES.md`(= `.hermes.md`) → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` 중 첫 매치 |

> ⚠️ **역할 오염 금지:** 파일 경로·컨벤션·명령 같은 작업 규칙 세부사항을 SOUL.md에 넣지 마세요. 반대로 말투·성격 같은 정체성을 HERMES.md에 넣지 마세요. 헷갈리면 위의 "한 줄 기준"으로 판단하세요.

## When to Use

- "SOUL.md를 만들고 싶어요" / "에이전트 말투·성격을 정하고 싶어요"
- "HERMES.md를 만들고 싶어요" / "이 에이전트의 작업 규칙을 정하고 싶어요"
- "에이전트에게 정체성을 주고 싶어요"
- "Hermes를 처음 써봐요. 뭘 설정해야 하나요?"

**Don't use for:** 이미 있는 파일의 아주 작은 한 줄 수정 — 직접 `read_file` → `patch`가 더 빠릅니다. (단, 여러 항목을 바꾸거나 어디를 고칠지 안내가 필요하면 이 스킬의 **Edit Mode**를 쓰세요.)

> 🔗 **새 프로필부터 만들어야 한다면** `create-hermes-profile` 스킬로 프로필을 만들고 model/tools/gateway를 셋업한 뒤, 그 프로필을 루트로 삼아 이 스킬을 이어서 실행하세요.

## Workflow

1. **두 파일의 역할을 쉽게 설명** (SOUL = 누구인가 / HERMES = 어떻게 일하는가). 아래 *Onboarding Introduction* 사용.
2. **대상 선택**: "SOUL만 / HERMES만 / 둘 다" 중 무엇을 만들지 고름.
3. **Pre-flight 점검**: 해당 파일이 이미 있는지 확인.
4. **모드 선택**: "간단히 / 자세히 / 프리셋 / 수정" 중 하나.
5. **질문**: 모드에 맞는 reference 파일을 읽어 **한 번에 하나씩**, 각 질문마다 예시를 곁들여 던짐.
6. **정리**: *Content Refinement*로 다듬고 완성본을 보여줌.
7. **저장**: 사용자가 동의하면 `scripts/save_hermes_md.py`로 **백업 후** 저장.
8. **마무리**: `/reset` 안내 + 테스트 문장 추천.

> "둘 다"면 SOUL.md를 먼저 완성한 뒤 "이제 작업 규칙(HERMES.md)을 정해볼게요!"라고 안내하고 이어서 진행합니다. 성격을 먼저 잡으면 작업 규칙의 톤이 일관됩니다.

## Pre-flight Check

질문을 시작하기 **전에**, 만들려는 파일이 이미 있는지 확인합니다. 건너뛰면 기존 설정을 모르고 덮어쓸 위험이 있습니다.

먼저 **루트 폴더**를 정합니다: `~/.hermes/profiles/` 아래에 프로필 폴더가 있으면 그 프로필 폴더가 루트, 없으면 `~/.hermes/`가 루트입니다. (SOUL.md와 HERMES.md 둘 다 이 폴더에 있습니다.)

- **SOUL.md** → `{루트}/SOUL.md`를 읽어봅니다.
- **HERMES.md** → `{루트}/HERMES.md` (또는 `{루트}/.hermes.md`)를 읽어봅니다.

**파일이 있을 때**: 내용을 간단히 요약해 보여주고 **수정(Edit Mode) / 새로 만들기(백업 후 교체) / 그만두기** 중 무엇을 할지 물어봅니다.
**파일이 없을 때**: 바로 환영 인사와 함께 온보딩을 시작합니다.

## Onboarding Introduction

스킬이 로드되면 먼저 아래처럼 쉽게 설명합니다:

> 안녕하세요! 🎉 지금부터 Hermes 에이전트를 나에게 맞게 설정해 볼 거예요.
>
> 설정 파일은 두 가지가 있어요. 역할이 서로 달라요:
> - **SOUL.md** 🧠 — 에이전트가 **누구인지** 정해요. 이름, 말투, 성격 같은 거예요. 한 번 정하면 **모든 곳에서** 그 성격으로 대화해요.
> - **HERMES.md** 📋 — 이 에이전트가 **어떻게 일할지** 정해요. 작업 규칙, 지켜야 할 컨벤션 같은 거예요. `CLAUDE.md`랑 비슷해요.
>
> 쉽게 말하면 **SOUL.md는 "성격", HERMES.md는 "업무 매뉴얼"** 이에요.
>
> 무엇을 만들까요? **"SOUL"**(성격/말투) · **"HERMES"**(작업 규칙) · **"둘 다"**(처음이면 추천!)

## Mode Selection

각 파일마다 진행 방식을 고를 수 있습니다.

- **간단히 (Essential)** — 필수 질문만 빠르게. → reference 파일의 *Essential* 섹션.
- **자세히 (Deep Dive)** — 심화 질문까지. → reference 파일의 *Deep Dive* 섹션.
- **프리셋 (Instant)** — 미리 만든 템플릿을 골라 즉시 완성. → `reference/presets.md`.
- **수정 (Edit)** — 기존 파일에서 특정 항목만 고치기. → 아래 *Edit Mode*.

## Content Refinement

질문이 끝나면 답변을 템플릿에 그대로 붙여넣지 마세요. **에디터처럼 정리한 뒤** 완성본을 보여주세요.

1. **중복 제거** — 비슷한 내용이 여러 답변에 흩어져 있으면 한 곳에만.
2. **통합** — 관련된 내용은 한 항목으로.
3. **다듬기** — 구어체를 깔끔한 문장으로. ("그냥 친근하게?" → "친근하고 가벼운 반말 톤")
4. **흐름 정리** — 간결하게. 두 파일 모두 에이전트가 매번 읽으므로 군더더기 최소화.
5. **자기완결성** — "아까 말한", "위에서" 같은 자기참조 제거.
6. **역할 점검 (중요)** — SOUL.md에 작업 규칙 세부사항(경로/명령/컨벤션)이 섞였는지, HERMES.md에 말투/성격이 섞였는지 확인하고 알맞은 파일로 옮기세요.

조립은 `reference/templates.md`를 사용합니다.

## Completion & Save Flow

### 1. Preview
완성본을 보여줍니다 (둘 다면 SOUL.md → HERMES.md 순서로):
> 완성됐어요! 🎉 마음에 드시나요? 수정하고 싶은 부분이 있으면 말씀해 주세요.

### 2. Edit if needed
사용자가 원하면 해당 부분을 바꿔줍니다.

### 3. Confirm save & 저장
저장 의사를 묻고, **저장 자체는 헬퍼 스크립트로** 수행합니다. 이 스크립트가 루트 해석·디렉터리 생성·타임스탬프 백업을 한 번에 처리하므로 백업 누락 같은 실수를 막아줍니다.

먼저 완성본을 임시 파일로 쓴 뒤(예: `write_file`로 `/tmp/SOUL.md`), 스크립트를 호출합니다:

```bash
# 프로필이 하나뿐이거나 ~/.hermes 직접 사용 → 자동 해석
python scripts/save_hermes_md.py --file SOUL.md --content-file /tmp/SOUL.md

# 프로필이 여러 개라 명시가 필요할 때
python scripts/save_hermes_md.py --file HERMES.md --profile myagent --content-file /tmp/HERMES.md

# 루트를 직접 지정
python scripts/save_hermes_md.py --file SOUL.md --root ~/.hermes/profiles/myagent --content-file /tmp/SOUL.md
```

- 프로필이 여러 개인데 `--profile`/`--root`가 없으면 스크립트가 **중단하고** 어느 프로필인지 물으라고 알려줍니다. 그때 사용자에게 물어보세요.
- 스크립트는 저장 결과를 JSON으로 출력합니다(`saved`, `backup`, `created_dir`). 백업이 생겼으면 사용자에게 경로를 알려주세요:
  > 기존 파일은 `SOUL.backup-...md`로 백업해 두었어요. 되돌리고 싶으면 이 파일을 쓰면 돼요.
- 저장 전 최종 경로를 사용자에게 확인받으세요: "{경로}에 저장하겠습니다. 괜찮으신가요?"

### 4. Post-save guidance
> ✅ 저장 완료!
>
> **중요:** 지금 바로 적용되지 않아요. 새 세션을 시작해야 해요. (`/reset` 또는 `hermes` 재실행)
> - 두 파일은 같은 루트 폴더에 함께 저장됐어요.
> - SOUL.md는 성격으로, HERMES.md는 작업 규칙으로 적용돼요.

### 5. Test suggestions
무엇을 만들었는지에 맞춰 테스트 문장을 추천합니다.
- SOUL.md: "안녕! 오늘 기분이 어때?" → 정한 말투·성격으로 답하는지 확인
- HERMES.md: 실제 작업을 하나 시켜보기 → 정한 작업 규칙을 따르는지 확인

## Edit Mode

기존 파일에서 **바꾸고 싶은 항목만** 고칩니다.

1. 기존 파일을 읽어 항목별로 요약해 보여줍니다.
2. 무엇을 바꿀지 물어봅니다 (여러 개 한 번에 가능).
3. 요청한 항목만 수정하고 **나머지는 그대로 보존**합니다.
4. **수정 전 → 수정 후**로 비교해 보여줍니다.
5. 확인되면 *Completion & Save Flow*로 (스크립트가 백업 포함).

**주의:** 사용자가 말하지 않은 항목은 절대 건드리지 마세요. 항목 삭제 전 한 번 더 확인. SOUL.md를 고치는데 작업 규칙 얘기가 나오거나 HERMES.md를 고치는데 말투 얘기가 나오면 "그건 {다른 파일}에 더 맞아요"라고 안내.

## Conversation Rules

- **한 번에 하나의 질문만.** 답변 후 짧게 받고 다음으로.
- **각 질문마다 최소 3~5개 예시** + 직접 입력 옵션 (reference 파일에 준비됨).
- **쉬운 말로.** "페르소나", "컨텍스트" 같은 용어는 풀어서. 초등학생도 이해할 수준으로.
- **격려를 섞어서.** ("좋은 이름이에요!", "딱 좋아요!")
- **모드 전환 허용.** "그냥 간단히 할래" / "Q3 다시" 등 중간 변경을 받아줌.
- **Skip with Defaults.** "몰라/넘어갈래" → 기본값 제시 후 진행. (이름 없음→"에이전트", 호칭 없음→"사용자님", 심화 질문은 생략)

## Common Pitfalls

1. **두 파일의 역할을 안 알려주고 시작함** — 가장 흔한 실수. 시작할 때 SOUL(누구)/HERMES(어떻게)를 꼭 구분해 설명하세요.
2. **역할 오염** — SOUL.md에 작업 규칙(경로/명령/컨벤션)을 넣거나, HERMES.md에 말투/성격을 넣음. Content Refinement의 역할 점검으로 걸러내세요.
3. **저장 위치 혼동** — SOUL.md와 HERMES.md는 **같은 루트 폴더**에 함께 둬야 합니다. 스크립트가 이를 보장합니다.
4. **Pre-flight Check 생략** — 기존 파일 확인 없이 덮어씀.
5. **백업 없이 덮어씀** — 저장은 반드시 `save_hermes_md.py`로. 손으로 저장하다 백업을 빠뜨리지 마세요.
6. **여러 질문을 한꺼번에 던짐** — 하나씩.
7. **완성 후 바로 저장** — 완성본을 먼저 보여주고 확인받기.
8. **`/reset` 안내 누락** — 새 세션에서만 로드됨.
9. **프리셋을 그대로 저장하고 끝냄** — 최소한 이름(SOUL)/역할·작업(HERMES)은 확인하고 바꿀 곳을 물어보세요.
10. **Edit Mode에서 시키지 않은 항목까지 고침** — 지정 항목만.

## Verification Checklist

- [ ] 시작 시 SOUL.md / HERMES.md의 역할 차이를 쉽게 설명했는가?
- [ ] 무엇을 만들지(SOUL만/HERMES만/둘 다) 선택받았는가?
- [ ] Pre-flight Check로 기존 파일 존재 여부를 확인했는가?
- [ ] 모드(간단히/자세히/프리셋/수정)를 설명하고 선택받았는가?
- [ ] 질문을 하나씩, 예시와 함께 던졌는가?
- [ ] Content Refinement로 정리하고 **역할 오염을 점검**했는가?
- [ ] 완성본을 보여주고 저장 의사를 확인했는가?
- [ ] `save_hermes_md.py`로 저장하여 같은 루트 폴더 + 백업이 보장됐는가?
- [ ] 저장 후 `/reset` 안내를 했는가?
- [ ] 테스트 문장을 추천했는가?
