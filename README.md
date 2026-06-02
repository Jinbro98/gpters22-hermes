# Hermes Skills — 프로필 & 정체성 셋업 팩

Hermes 에이전트를 **처음부터 셋업**하기 위한 스킬 2개를 담은 스킬 팩입니다.
질문에 답하기만 하면, 봇을 담을 **프로필**을 만들고 그 안에 봇의 **성격·작업 규칙**까지 채울 수 있습니다.

| 스킬 | 한 줄 설명 | 무엇을 만드나 |
|---|---|---|
| [`create-hermes-profile`](./create-hermes-profile/SKILL.md) | 인터뷰로 새 프로필을 만들고 모델·도구·게이트웨이까지 셋업 | 봇의 **그릇(프로필)** |
| [`hermes-md-wizard`](./hermes-md-wizard/SKILL.md) | 대화로 `SOUL.md`(정체성)·`HERMES.md`(작업 규칙)를 작성 | 그릇 안의 **성격·규칙** |

두 스킬은 이어집니다 — `create-hermes-profile`로 프로필을 만든 뒤, 그 프로필을 루트로 `hermes-md-wizard`가 정체성을 입힙니다.

---

## 설치 (Install)

각 스킬 폴더를 전역 스킬 디렉터리 **`~/.hermes/skills/`** 에 복사하면 됩니다.

### macOS · Linux

```bash
git clone https://github.com/Jinbro98/hermes-md-wizard.git
cd hermes-md-wizard

mkdir -p ~/.hermes/skills
cp -R create-hermes-profile ~/.hermes/skills/
cp -R hermes-md-wizard     ~/.hermes/skills/
```

### Windows (PowerShell)

```powershell
git clone https://github.com/Jinbro98/hermes-md-wizard.git
Set-Location hermes-md-wizard

New-Item -ItemType Directory -Force "$HOME/.hermes/skills" | Out-Null
Copy-Item -Recurse -Force create-hermes-profile "$HOME/.hermes/skills/"
Copy-Item -Recurse -Force hermes-md-wizard     "$HOME/.hermes/skills/"
```

> ⚠️ 같은 이름의 스킬이 이미 있으면 덮어쓰기 전에 백업하세요.
> 폴더 구조(`SKILL.md` + `scripts/` · `reference/` · `examples/`)는 **그대로** 유지해야 합니다.

설치 후 디렉터리:

```
~/.hermes/skills/
├── create-hermes-profile/
│   ├── SKILL.md
│   └── scripts/verify_profile.py
└── hermes-md-wizard/
    ├── SKILL.md
    ├── reference/   (질문·프리셋·템플릿)
    ├── examples/    (SOUL/HERMES 샘플)
    └── scripts/save_hermes_md.py
```

### 요구 사항

- **Hermes Agent CLI** — `create-hermes-profile`가 실제 `hermes` 명령을 실행합니다.
- **Python 3** — 번들 헬퍼 스크립트용. 표준 라이브러리만 사용하므로 `pip install`이 필요 없습니다.

---

## 사용 (Usage)

설치 후 **새 Hermes 세션**을 시작하면 스킬이 로드됩니다. 그다음 자연어로 요청하면 됩니다.

```
"Hermes 프로필 새로 만들어줘"        → create-hermes-profile 발동
"이 에이전트 성격이랑 규칙 잡아줘"   → hermes-md-wizard 발동
```

자세한 동작·규칙은 각 스킬의 `SKILL.md`를 참고하세요.

---

## 이 레포를 에이전트에게 설치 시키려면

레포 링크를 에이전트에게 주고 "설치해줘"라고 할 수 있도록 [`AGENTS.md`](./AGENTS.md)에 에이전트용 설치 프로토콜이 정리돼 있습니다.

## 라이선스

MIT
