---
name: create-hermes-profile
description: "Use when creating and initializing a Hermes Agent profile through an interview-driven workflow: choose creation mode, run model/tools/gateway setup in PTY, start the profile gateway, and verify profile/gateway state without changing the sticky default profile."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Hermes, Profiles, Gateway, Setup, Multi-Agent]
    related_skills: [hermes-agent]
---

# Create Hermes Profile

## Overview

Hermes Agent 프로필을 새로 만들고, 모델/도구/게이트웨이 초기 설정까지 진행할 때 사용하는 스킬입니다. 이 스킬의 핵심은 **인터뷰 우선**입니다. 프로필 이름, 생성 방식, 모델/도구/게이트웨이 선택, 토큰 처리, 충돌 처리처럼 결과가 달라지는 값은 절대 추측하지 말고 사용자에게 확인합니다.

기본 생성 명령은 `hermes profile create NAME`입니다. 이 명령은 fresh profile을 만들고 bundled skills를 seed합니다. 사용자가 “정말 skills도 없는 빈 프로필”을 원한다고 명시한 경우에만 `--no-skills`를 별도로 확인한 뒤 사용합니다.

## When to Use

- 사용자가 “Hermes 프로필 새로 만들어줘”, “새 에이전트 프로필 세팅해줘”, “새 봇 프로필 만들자”라고 요청할 때
- 새 프로필 생성 후 `model`, `tools`, `gateway` 설정까지 한 흐름으로 끝내야 할 때
- Kanban/멀티 프로필 운영을 위해 역할별 Hermes profile을 추가할 때
- 프로필 생성 모드를 fresh/clone/clone-all/clone-from 중에서 사용자에게 물어야 할 때

Do **not** use this skill for:

- 기존 프로필 삭제/rename/export/import만 하는 작업
- profile workspace 경로 이동 또는 wiki relocation 작업
- Hermes 자체 설치/업데이트/소스코드 수정 작업 전반. 그런 경우 `hermes-agent` 스킬을 함께 로드합니다.

## Non-Negotiable Rules

1. **가정 금지:** 프로필 이름, 생성 모드, source profile, 역할 설명, 모델/provider, toolsets, gateway platform, gateway token, gateway start 여부를 추측하지 않습니다.
2. **기본 프로필 변경 금지:** 이 스킬은 `hermes profile use NAME`을 실행하지 않습니다. 새 프로필을 만들고 설정만 합니다.
3. **충돌 시 중단:** 요청한 profile name이 이미 존재하면 삭제/덮어쓰기/자동 suffix 생성을 하지 말고, 사용자에게 새 이름을 물어봅니다.
4. **비밀값 취급:** 사용자가 채팅에 토큰/API key를 제공하면 해당 profile의 `.env`에 저장할 수 있습니다. 단, 최종 응답과 로그 요약에 비밀값을 그대로 노출하지 않습니다.
5. **Gateway는 설정 후 시작:** model/tools/gateway setup이 끝나면 `hermes --profile NAME gateway start`를 실행합니다.
6. **검증 필수:** 완료 전 `profile show`, `config check`, `tools list`, `gateway status`, gateway log 확인을 수행합니다.

## Required Interview

작업을 시작하기 전에 아래 항목을 사용자에게 확인합니다. 사용자가 이미 명확히 말한 항목은 다시 묻지 않아도 됩니다.

1. **Profile name**
   - 예: `researcher`, `finance-bot`, `podo2`
   - 허용 형식: `[a-z0-9][a-z0-9_-]{0,63}`
   - `default`, `hermes`, `test`, `tmp`, `root`, `sudo` 같은 예약/혼동 이름은 피합니다.

2. **Creation mode**
   - Fresh default: `hermes profile create NAME`
   - Fresh without bundled skills: `hermes profile create NAME --no-skills`
   - Clone config/skills from active profile: `hermes profile create NAME --clone`
   - Clone all state from active profile: `hermes profile create NAME --clone-all`
   - Clone from a specific source profile: `hermes profile create NAME --clone-from SOURCE`
   - Clone all from a specific source profile: `hermes profile create NAME --clone-all --clone-from SOURCE`

3. **Optional profile description**
   - 비워도 진행합니다.
   - 사용자가 설명을 주면 생성 시 `--description "..."`를 붙이거나, 생성 후 `hermes profile describe NAME --text "..."`를 실행합니다.
   - 설명은 Kanban decomposer가 역할 기반 라우팅에 사용할 수 있으므로 있으면 좋지만 필수는 아닙니다.

4. **Model setup preference**
   - provider/model을 사용자가 알고 있으면 기록하고 setup wizard에서 반영합니다.
   - 모르면 `hermes --profile NAME setup model`의 대화형 wizard에서 고르게 합니다.

5. **Tool setup preference**
   - 필요한 toolsets를 묻습니다.
   - 모르면 `hermes --profile NAME setup tools`에서 고르게 합니다.
   - tool 변경은 새 세션부터 적용될 수 있음을 알려줍니다.

6. **Gateway setup preference**
   - 사용할 platform: Telegram, Discord, Slack, Kakao bridge, API server 등
   - 필요한 token/API key/allowed users/home channel
   - 사용자가 채팅으로 비밀값을 제공할지, wizard에 직접 입력할지 확인합니다.

## Workflow

### 1. Preflight

```bash
hermes profile list
hermes profile create --help
```

- `hermes profile list`로 기존 프로필을 확인합니다.
- 같은 이름이 있으면 여기서 중단하고 사용자에게 새 이름을 물어봅니다.
- `hermes profile create --help`로 현재 설치된 Hermes CLI의 옵션을 확인합니다. CLI 옵션은 버전에 따라 달라질 수 있습니다.

### 2. Build the Create Command

사용자의 답변으로 명령을 구성합니다. 예시는 다음과 같습니다.

```bash
# Fresh default profile, bundled skills included
hermes profile create NAME

# Fresh profile with no bundled skills
hermes profile create NAME --no-skills

# Copy config.yaml, .env, SOUL.md, skills, and selected identity files from active profile
hermes profile create NAME --clone

# Full copy of active profile state
hermes profile create NAME --clone-all

# Copy from a specific source profile
hermes profile create NAME --clone-from SOURCE

# Full copy from a specific source profile
hermes profile create NAME --clone-all --clone-from SOURCE

# Optional description at creation time
hermes profile create NAME --description "one- or two-sentence role description"
```

Notes:

- `--no-skills` is mutually exclusive with clone modes. If the user asks for both, stop and ask which is more important.
- `--clone-all` can carry substantial state from the source profile. Use only when the user explicitly chooses it.
- Do not add `--no-alias` unless the user explicitly asks to skip wrapper alias creation.

### 3. Create the Profile

```bash
hermes profile create NAME [...selected flags...]
```

If creation fails:

- Do not delete anything automatically.
- Show the non-secret error summary.
- Ask the user how to proceed.

### 4. Optional Description

If the user provided a description and it was not included in the create command:

```bash
hermes profile describe NAME --text "one- or two-sentence role description"
```

If the user skipped description, continue without it.

### 5. Interactive Setup via PTY

Run setup sections one at a time in PTY. For interactive sessions, prefer background PTY so prompts can be read and answered deliberately.

```bash
hermes --profile NAME setup model
hermes --profile NAME setup tools
hermes --profile NAME setup gateway
```

Recommended Hermes tool pattern:

```python
terminal(command="hermes --profile NAME setup model", pty=True, background=True)
process(action="poll", session_id="...")
process(action="submit", session_id="...", data="user answer")
```

Repeat for `tools` and `gateway`.

During setup:

- Relay ambiguous wizard prompts to the user instead of guessing.
- If the prompt asks for a token/API key and the user provides it in chat, submit or write it only to the target profile’s config/env path.
- Do not include full tokens/API keys in final summaries.
- If setup becomes stuck, close/kill only the setup process for the target profile, not unrelated profile gateways.

### 6. Start Gateway

After gateway setup completes:

```bash
hermes --profile NAME gateway start
```

Avoid `--all` unless the user explicitly asks, because it can kill stale gateway processes across profiles.

### 7. Verify

Run all checks before reporting success.

```bash
hermes profile show NAME
hermes --profile NAME config check
hermes --profile NAME tools list
hermes --profile NAME gateway status
hermes --profile NAME logs gateway --since 10m -n 100
```

Interpretation:

- `profile show` should point at `~/.hermes/profiles/NAME/`.
- `config check` should not report missing model/provider essentials.
- `tools list` should reflect the selected toolsets.
- `gateway status` should show the profile gateway as running/healthy when supported by the host.
- Gateway logs should show platform connection or a clear actionable warning/error.

## Final Response Format

Keep the final response concise and operational.

```markdown
지녕님, 새 Hermes 프로필 생성/설정 완료했습니다.

- Profile: `NAME`
- Path: `~/.hermes/profiles/NAME/`
- Creation mode: `fresh default` / `clone` / `clone-all` / `clone-from SOURCE`
- Description: 저장함 / 건너뜀
- Model setup: 완료 / 확인 필요
- Tools setup: 완료 / 확인 필요
- Gateway: started / failed / needs user action
- Gateway log check: 이상 없음 / 경고 N개
- Default profile: 변경하지 않음

다음 사용 예:
`hermes --profile NAME chat`
```

Never print secrets in the final response.

## Common Pitfalls

1. **“빈 프로필”의 의미 혼동**
   - `hermes profile create NAME`은 fresh profile이지만 bundled skills를 seed합니다.
   - skills도 없는 strict empty profile은 `--no-skills`가 필요합니다. 반드시 사용자에게 확인합니다.

2. **기본 프로필을 실수로 바꿈**
   - `hermes profile use NAME`은 sticky default를 바꿉니다. 이 스킬에서는 실행하지 않습니다.

3. **이미 있는 이름을 덮어쓰려 함**
   - Hermes profile create는 기존 directory가 있으면 실패합니다. 삭제/덮어쓰기는 이 스킬 범위 밖입니다.

4. **Clone mode와 `--no-skills` 충돌**
   - clone은 source profile의 skills를 복사합니다. `--no-skills`와 함께 쓰지 않습니다.

5. **Gateway token 노출**
   - 사용자가 채팅에 토큰을 제공할 수는 있지만, 최종 응답/로그 요약에는 절대 노출하지 않습니다.

6. **Gateway setup만 하고 start를 빼먹음**
   - 이 스킬은 설정 후 `hermes --profile NAME gateway start`까지 수행합니다.

7. **Gateway가 시작됐지만 플랫폼이 조용함**
   - Telegram/Discord 등은 BotFather/Developer Portal 권한, allowed users, home channel, mention/privacy 설정 문제일 수 있습니다. `hermes --profile NAME logs gateway --since 10m -n 100`로 원인을 확인합니다.

8. **Tool changes not visible immediately**
   - 도구/스킬 설정 변경은 새 Hermes session부터 적용될 수 있습니다. 필요하면 새 세션으로 테스트합니다.

## Verification Checklist

- [ ] User confirmed profile name
- [ ] User confirmed creation mode
- [ ] Existing profile collision checked with `hermes profile list`
- [ ] Profile created with selected `hermes profile create` command
- [ ] Optional description saved or explicitly skipped
- [ ] `hermes --profile NAME setup model` completed
- [ ] `hermes --profile NAME setup tools` completed
- [ ] `hermes --profile NAME setup gateway` completed
- [ ] `hermes --profile NAME gateway start` executed
- [ ] `hermes profile show NAME` verified
- [ ] `hermes --profile NAME config check` verified
- [ ] `hermes --profile NAME tools list` verified
- [ ] `hermes --profile NAME gateway status` verified
- [ ] `hermes --profile NAME logs gateway --since 10m -n 100` checked
- [ ] Final response redacts secrets
- [ ] `hermes profile use NAME` was not executed
