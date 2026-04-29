# LOADSTAR_INIT — loadstar_mcp

> AI 세션 진입 시 이 파일을 읽어 프로젝트 컨텍스트를 복원합니다.

## 프로젝트 개요

- **언어/스택**: Python 3.10+ + 공식 [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **전송 방식**: stdio (1차), 향후 Streamable HTTP 추가 가능
- **배포**: `uvx loadstar-mcp` 또는 `pip install loadstar-mcp`
- **CLI 의존**: `loadstar.exe` — subprocess 호출 (시스템 PATH 또는 `LOADSTAR_CLI_PATH`)
- **SPEC 문서**: `loadstar_SPEC` (`LOADSTAR_SPEC_PATH` 환경변수)

## 설계 원칙 (확정 결정)

- **Stateless** — MCP 서버는 워크스페이스 상태를 보유하지 않는다
- **project_path 의무 입력** — 모든 도구(get_spec 제외)는 절대경로를 의무 인자로 받는다
- **CLI 얇은 래퍼** (DRAFT §3) — 새 비즈니스 로직 금지. CLI subprocess + JSON 정형화
- **CLI 미존재 도구만 직접 파일 읽기** — `get_waypoint`, `get_map`, `get_spec` 한정
- **언어 중립적 도구 명세** — 향후 Go 포팅 시 외부 클라이언트 영향 없도록

## 환경변수

| 이름 | 필수 | 용도 |
|:--|:--|:--|
| `LOADSTAR_CLI_PATH` | 선택 | `loadstar` 바이너리 경로. 미설정 시 시스템 PATH 탐색 |
| `LOADSTAR_SPEC_PATH` | 선택 | `loadstar_get_spec` 호출 시에만 필요. SPEC 저장소 경로 |

## AI 참고사항

- 본 저장소는 LOADSTAR MCP 서버 1차 구현 (Python). 외부 클라이언트(Claude Desktop, Cursor, Cline, 웹 Claude.ai) 이식성 확보가 목적.
- 언어 결정: Go → Python 변경 (DRAFT §2 갱신). 이유: 공식 SDK 성숙도, 외부 진입 장벽, 얇은 래퍼라 정확도 무관.
- 외부 사용 검증 후 Go 포팅 검토 가능.

## 최근 변경

- 2026-04-29 저장소 생성 + LOADSTAR init + W://root/mcp_server 등록
- 2026-04-29 설계 확정: Stateless + project_path 의무 입력 (Q1/Q2 RESOLVED inline)
