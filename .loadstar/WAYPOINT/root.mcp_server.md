<WAYPOINT>
## [ADDRESS] W://root/mcp_server
## [STATUS] S_PRG

### IDENTITY
- SUMMARY: LOADSTAR MCP 서버 1차 구현 완료 (Python + 공식 mcp SDK, stdio). Stateless 설계 — 모든 도구가 project_path(절대경로) 의무 인자. 10개 도구 구현 완료. PyPI 이름 확인 + 스모크 테스트 대기 중.
- METADATA: [Priority: P1, Created: 2026-04-29]
- SYNCED_AT: 2026-04-29

### CONNECTIONS
- PARENT: M://root
- CHILDREN: []
- REFERENCE: []

### CODE_MAP
- scope:
  - src/loadstar_mcp/

### TODO
# TASK — 프로젝트 스캐폴드
- [x] 2026-04-29 pyproject.toml 작성 (의존: mcp, pydantic) + uv 호환 + entry point `loadstar-mcp`
- [x] 2026-04-29 src/loadstar_mcp/__init__.py
- [x] 2026-04-29 src/loadstar_mcp/server.py — MCP 서버 entry point (stdio)
- [x] 2026-04-29 src/loadstar_mcp/paths.py — project_path 검증(절대경로/디렉토리 존재/.loadstar 보유), SPEC_PATH/CLI_PATH 환경변수 처리
- [x] 2026-04-29 src/loadstar_mcp/cli.py — loadstar CLI subprocess 래퍼 (cwd=project_path, 타임아웃, 에러 처리)
- [x] 2026-04-29 src/loadstar_mcp/elements.py — WP/Map md 파일 파서 (CODE_MAP.scope 포함)
- [x] 2026-04-29 README.md — 설치 가이드(`uvx loadstar-mcp`) + 환경변수(`LOADSTAR_CLI_PATH` 선택, `LOADSTAR_SPEC_PATH` 선택) + 사용 예시(절대경로 명시 패턴)
- [x] 2026-04-29 .gitignore (Python)
- [x] 2026-04-29 LICENSE (Apache 2.0, SPEC와 동일)

# TASK — CLI 래핑 도구 (DRAFT §4) — 모든 도구 project_path 필수
- [x] 2026-04-29 loadstar_show(project_path: str, filter: str | None = None)
- [x] 2026-04-29 loadstar_validate(project_path: str)
- [x] 2026-04-29 loadstar_todo_list(project_path: str)
- [x] 2026-04-29 loadstar_todo_history(project_path: str, map: str | None = None)
- [x] 2026-04-29 loadstar_log(project_path: str, time_range: str | None = None, filter: str | None = None)
- [x] 2026-04-29 loadstar_log_add(project_path: str, address: str, kind: str, content: str)
- [x] 2026-04-29 loadstar_question(project_path: str, filter: str | None = None, with_resolved: bool = False)

# TASK — 직접 파일 읽기 도구 (DRAFT §4)
- [x] 2026-04-29 loadstar_get_waypoint(project_path: str, address: str) — CODE_MAP.scope 정확 추출
- [x] 2026-04-29 loadstar_get_map(project_path: str, address: str)
- [x] 2026-04-29 loadstar_get_spec(section: str | None = None) — `LOADSTAR_SPEC_PATH` 사용, project_path 미수령

# TASK — 검증 / 에러 처리
- [x] 2026-04-29 project_path 검증 — 절대경로 / 디렉토리 존재 / `.loadstar/` 보유 — 실패 시 명확 에러
- [x] 2026-04-29 CLI 호출 실패 / 타임아웃 / non-zero exit 표준 에러 형식
- [x] 2026-04-29 LOADSTAR_SPEC_PATH 미설정인데 get_spec 호출 시 안내성 에러
- [x] 2026-04-29 subprocess.run에 encoding="utf-8" 명시 — Windows 기본 cp949로 한글 WP 출력 디코딩 실패 시 stdout=None 반환되어 MCP Pydantic string_type 에러 발생
- [x] 2026-04-29 도구 description 정정 — log_add KIND 실제 허용값(NOTE/DECISION/ISSUE/RESOLVED/PROGRESS/MODIFIED) 명시, show filter는 address만 매칭, log time_range는 Nd/Nh 형식만 지원 (CLI help 기준)

# TASK — 도구 description (DRAFT §6)
- [x] 2026-04-29 모든 project_path 받는 도구에 표준 문구: "absolute path to the project root (must contain .loadstar/)"
- [x] 2026-04-29 WayPoint 작업 규칙(착수 전 체크 / 완료 후 체크 / S_IDL→S_PRG→S_STB) description에 인코딩
- [x] 2026-04-29 CODE_MAP.scope 활용 흐름 → get_waypoint description에서 후속 LSP/grep 인자 활용 안내

# TASK — 의도적 제외 검증
- [x] 2026-04-29 loadstar_check, loadstar_init, loadstar_todo_sync, loadstar_list_projects 노출 안 함 (server.py에 미등록)

# TASK — 문서/배포
- [ ] PyPI 패키지 이름 확인 (loadstar-mcp 충돌 여부)
- [x] 2026-04-29 Claude Desktop 설치 예시 (claude_desktop_config.json 스니펫) — README.md
- [x] 2026-04-29 Claude Code 설치 예시 (`claude mcp add loadstar -- uvx loadstar-mcp`) — README.md

# RECURRING
- (R) 변경 후 `python -m loadstar_mcp.server` 로컬 stdio 실행 검증
- (R) MCP Inspector(`npx @modelcontextprotocol/inspector`) 또는 Claude Code 등록으로 도구 호출 스모크 테스트
- (R) DRAFT §4 도구 명세 변경 시 CLAUDE.md 노출 도구 목록 표 동기화

### ISSUE
- OPEN_QUESTIONS:
  - [Q1 RESOLVED inline] Stateless 설계 — 모든 도구가 project_path(절대경로)를 의무 인자로 받는다. 환경변수 폴백·워크스페이스 발견 메커니즘 없음. SPEC 경로만 LOADSTAR_SPEC_PATH 환경변수로 별도 관리. (Decision 파일 미생성 — 인라인 결정)
  - [Q2 RESOLVED inline] 다중 프로젝트는 호출 시 다른 project_path를 전달하면 자연 지원. 등록·발견 메커니즘 불필요 — `.loadstar/`가 곧 프로젝트 진실. loadstar_list_projects/loadstar_init은 노출하지 않음. (Decision 파일 미생성 — 인라인 결정)

### COMMENT
- DRAFT §3 원칙: CLI 호출이 정답. 새 비즈니스 로직 만들지 말 것.
- 도구 description은 영어 1차(외부 클라이언트 다국어 사용자 다수). 추후 i18n 검토.
- 첫 동작 우선 4개: show, validate, get_waypoint, get_spec — 실제 사용 빈도 최상위.
- Stateless 트레이드오프: 외부 사용자가 매 호출 절대경로 명시 부담이 있으나, 사용자가 자기 프로젝트 위치를 안다는 자연스러운 전제. README 첫 줄에 패턴 안내.
</WAYPOINT>
