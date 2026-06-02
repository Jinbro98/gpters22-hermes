# AGENTS.md — 설치 프로토콜 (에이전트용)

이 레포는 **Hermes 에이전트 스킬 팩**입니다. 사용자가 이 레포를 가리키며 "설치해줘"라고 하면, 아래 절차를 그대로 따르세요.

## 이 레포에 들어 있는 것

최상위에 `SKILL.md`를 가진 폴더가 **각각 하나의 스킬**입니다. 현재 2개:

- `create-hermes-profile/` — 인터뷰로 Hermes 프로필 생성 + 모델·도구·게이트웨이 셋업
- `hermes-md-wizard/` — 대화로 `SOUL.md`(정체성)·`HERMES.md`(작업 규칙) 작성

각 스킬 폴더는 `SKILL.md`와 하위 폴더(`scripts/`, `reference/`, `examples/`)로 구성됩니다. **빌드 단계는 없습니다.**

## 설치 절차

**대상 경로:** 전역 스킬 디렉터리 `~/.hermes/skills/`

1. **스킬 폴더 식별** — 레포 최상위에서 `SKILL.md`를 직접 포함한 디렉터리를 모두 찾습니다. (이 문서·`README.md`·`.git/` 등은 스킬이 아닙니다.)
2. **대상 디렉터리 준비** — `~/.hermes/skills/`가 없으면 만듭니다.
3. **충돌 확인** — `~/.hermes/skills/<스킬이름>/`이 이미 있으면, **덮어쓰지 말고** 사용자에게 덮어쓸지/건너뛸지 물어봅니다. 덮어쓴다면 기존 폴더를 먼저 백업합니다.
4. **복사** — 각 스킬 폴더를 하위 구조(`SKILL.md` + `scripts/`·`reference/`·`examples/`)를 **그대로 유지**한 채 `~/.hermes/skills/`로 복사합니다.
5. **검증** — `~/.hermes/skills/<스킬이름>/SKILL.md`가 존재하고, 하위 폴더가 빠지지 않았는지 확인합니다.
6. **안내** — 설치된 스킬 이름을 사용자에게 보고하고, **새 Hermes 세션**을 시작해야 로드된다고 알립니다.

### 복사 명령 예시

macOS · Linux:

```bash
mkdir -p ~/.hermes/skills
cp -R create-hermes-profile ~/.hermes/skills/
cp -R hermes-md-wizard     ~/.hermes/skills/
```

Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force "$HOME/.hermes/skills" | Out-Null
Copy-Item -Recurse -Force create-hermes-profile "$HOME/.hermes/skills/"
Copy-Item -Recurse -Force hermes-md-wizard     "$HOME/.hermes/skills/"
```

> 폴더 이름을 임의로 바꾸지 마세요. `SKILL.md`의 `name` 필드와 폴더명이 일치해야 합니다.

## 주의

- **새 폴더만 추가**하세요. `~/.hermes/skills/` 안의 다른 무관한 스킬을 건드리거나 지우지 마세요.
- 스크립트는 **Python 3 표준 라이브러리만** 사용합니다. `pip install`이나 의존성 설치가 필요 없습니다.
- `create-hermes-profile`를 실제로 **실행**하려면 시스템에 **Hermes CLI**가 설치돼 있어야 합니다(설치 자체에는 불필요).
- 사용자에게 비밀값(토큰/API 키)을 요구하거나 출력하지 마세요. 설치는 파일 복사일 뿐입니다.

## 설치 후

사용자는 새 세션에서 다음처럼 호출할 수 있습니다:

- "Hermes 프로필 새로 만들어줘" → `create-hermes-profile`
- "에이전트 성격·규칙 잡아줘" → `hermes-md-wizard`
