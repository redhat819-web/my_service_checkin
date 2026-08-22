# my_service GitHub 업로드 가이드

`my_service` 전체(backend + frontend)를 하나의 레포로 GitHub에 올리는 과정입니다.

## 사전 준비
- GitHub에서 빈 레포 생성 (README·.gitignore 없이 완전히 빈 상태 권장)
- 레포 주소: `https://github.com/lubl-ai/my_service.git`

## 1. 원격 레포 연결
```bash
# 아직 연결 안 된 경우
git remote add origin https://github.com/lubl-ai/my_service.git

# 이미 origin이 있는데 주소만 바꾸려면
git remote set-url origin https://github.com/lubl-ai/my_service.git

# 연결 확인
git remote -v
```

## 2. 변경사항 스테이징 & 커밋
```bash
# my_service 폴더 전체를 통째로 추가
git add -A

# 상태 확인
git status

# 커밋
git commit -m "Upload my_service (backend + frontend)"
```

## 3. 브랜치 정리 & Push
```bash
# 기본 브랜치를 main으로
git branch -M main

# 최초 push (-u 로 업스트림 설정)
git push -u origin main
```

## 4. 이후 작업 (2번째부터)
```bash
git add -A
git commit -m "변경 내용 설명"
git push
```

## 참고
- **인증**: HTTPS면 push 시 GitHub 토큰(PAT) 입력. SSH 쓰려면 주소를 `git@github.com:lubl-ai/my_service.git`로 변경.
- **빈 레포가 아닐 때**: 원격에 커밋이 있어 push가 거부되면 `git pull origin main --rebase` 후 다시 push.
- **.gitignore 확인**: `venv/`, `__pycache__/`, `.env` 등 불필요/민감 파일이 제외되는지 push 전에 확인.
