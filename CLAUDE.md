# LOADSTAR MCP — Claude Agent 운영 규칙

## 세션 시작 절차

1. 이 파일을 읽는다.
2. `.loadstar/LOADSTAR_INIT.md` 를 읽어 현재 프로젝트 상태를 파악한다.
3. 작업이 SPEC 변경/MCP 도구 명세 결정과 관련되면 `C:\bono\MCP\GIT\loadstar_SPEC\internal\MCP_DESIGN_DRAFT.md`를 추가로 읽는다.

---

## 프로젝트 개요

- **언어**: Python 3.10+
- **MCP SDK**: 공식 [`mcp`](https://github.com/modelcontextprotocol/python-sdk) (Anthropic)
- **저장소**: `C:\bono\MCP\GIT\loadstar_mcp\`
- **CLI 의존**: `C:\bono\MCP\GIT\loadstar_cli\bin\loadstar.exe` (subprocess 호출)
- **SPEC 문서**: `C:\bono\MCP\GIT\loadstar_SPEC\`

---

## WayPoint 작업 규칙 (필수)

### 작업 전
1. 대상 WayPoint를 확인한다 (`.loadstar/WAYPOINT/` 하위)
2. TODO에 작업 항목이 없으면 `- [ ] 작업 내용`을 추가한다
3. STATUS가 `S_IDL`이면 `S_PRG`로 변경한다

### 작업 후
1. 완료된 TODO 항목을 `- [x] YYYY-MM-DD 작업 내용`으로 체크한다
2. WP의 모든 TODO TASK 항목이 완료되면 STATUS를 `S_STB`로 변경한다
3. SUMMARY가 현재 기능과 다르면 갱신한다

### 원칙
- **항목 없이 코드 수정 금지** — 먼저 WayPoint에 "무엇을 할 것인가"를 기록
- 빠른 버그 수정의 경우 코드 수정 후 사후 등록도 허용

---

## MCP 구현 원칙 (확정)

- **Stateless** — MCP 서버는 워크스페이스 상태를 보유하지 않음
- **project_path 의무 입력** — 모든 도구(get_spec 제외)는 절대경로를 의무 인자로 받음
- **CLI 얇은 래퍼 우선** (DRAFT §3) — 새 비즈니스 로직 금지. CLI 호출 + JSON 정형화
- **직접 파일 읽기는 예외만** — `get_waypoint`, `get_map`, `get_spec` 한정
- **언어 중립적 도구 스키마** — 향후 Go 포팅 시 그대로 사용 가능
- **도구 description에 워크플로 인코딩** (DRAFT §6) — CLAUDE.md가 닿지 않는 외부 클라이언트가 도구 description으로 LOADSTAR 흐름 학습

## 노출 도구 목록

| 도구 | 시그니처 | 구현 |
|:--|:--|:--|
| `loadstar_show` | `(project_path, filter?)` | CLI 래핑 |
| `loadstar_validate` | `(project_path)` | CLI 래핑 |
| `loadstar_todo_list` | `(project_path)` | CLI 래핑 |
| `loadstar_todo_history` | `(project_path, map?)` | CLI 래핑 |
| `loadstar_log` | `(project_path, time_range?, filter?)` | CLI 래핑 |
| `loadstar_log_add` | `(project_path, address, kind, content)` | CLI 래핑 |
| `loadstar_question` | `(project_path, filter?, with_resolved?)` | CLI 래핑 |
| `loadstar_get_waypoint` | `(project_path, address)` | 직접 파일 읽기 |
| `loadstar_get_map` | `(project_path, address)` | 직접 파일 읽기 |
| `loadstar_get_spec` | `(section?)` | 직접 파일 읽기 (`LOADSTAR_SPEC_PATH`) |

**의도적 제외**: `loadstar_check`, `loadstar_init`, `loadstar_todo_sync`, `loadstar_list_projects` (DRAFT §5 + Stateless 결정)

---

## 환경변수

| 이름 | 필수 | 용도 |
|:--|:--|:--|
| `LOADSTAR_CLI_PATH` | 선택 | `loadstar` 바이너리 경로. 미설정 시 시스템 PATH 탐색 |
| `LOADSTAR_SPEC_PATH` | 선택 | `loadstar_get_spec` 호출 시에만 필요 |

## 주소 체계

```
M://root              →  .loadstar/MAP/root.md
W://root/mcp_server   →  .loadstar/WAYPOINT/root.mcp_server.md
```
