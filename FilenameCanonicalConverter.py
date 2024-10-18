#################################
# FilenameCanonicalConverter.py #
#################################

import os
import argparse
import unicodedata
import shutil
import glob

def normalize_name_in_path(path, form):
    """
    주어진 파일 경로에서 파일명 부분만 유니코드 캐노니컬 변환하는 함수
    """
    # 경로에서 디렉토리 경로와 파일명 분리
    dir_path, name = os.path.split(path)
    
    # 파일명을 form 형식으로 변환
    decomposed_name = unicodedata.normalize(form, name)
    
    # 다시 디렉토리 경로와 변환된 파일명을 합쳐 새로운 경로 생성
    new_path = os.path.join(dir_path, decomposed_name)

    if path == new_path:
        print(f"passed: '{path}' ({len(path)})")
        return None

    try:
        # shutil.move()는 파일 및 디렉토리 모두 이동 가능
        shutil.move(path, new_path)
        print(f"success:'{path}' {form}: ({len(path)}) -> ({len(new_path)})")
    except FileNotFoundError:
        print(f"ERROR:  '{path}' Not Found")
    except PermissionError:
        print(f"ERROR:  '{path}' 에 접근할 수 있는 권한이 없습니다.")
    except Exception as e:
        print(f"Encountered: {e}")
    
    return new_path

def main():
    # argparse로 명령어 인자 받기
    parser = argparse.ArgumentParser(description="지정된 파일명을 유니코드 형식 변경")

    # 두 가지의 유니코드 변환 방식 (-compose/--C와 -decompose/--D)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--compose', '-C', action='store_true', help="유니코드 (조립된) 완성형으로 변환 (NFC) (기본값)")
    group.add_argument('--decompose', '-D', action='store_true', help="유니코드 (분해된) 조합형으로 변환 (NFD)")

    # path 인자를 추가 (와일드카드 패턴을 사용할 수 있음)
    parser.add_argument('path', default='*', help="파일 경로 패턴 (와일드카드 사용 가능)")

    args = parser.parse_args()

    # 유니코드 변환 형식 설정
    if True == args.decompose:
        form = 'NFD'  # 유니코드 분해형 
    else:
        form = 'NFC'  # 유니코드 조합형

    # 대상 파일 목록 설정
    paths = glob.glob(args.path)

    # print("compose:", args.compose)
    # print("decompose:", args.decompose)
    # print("path:", args.path)
    # print("glob:", paths)

    if len(paths) == 0:
        print(f"오류: '{args.path}' 파일이 존재하지 않습니다.")
    else:
        for path in paths:
            normalize_name_in_path(path, form=form)

if __name__ == "__main__":
    main()
