import copy

SET_A = [1, 2, 3, 4, 5]
N = len(SET_A)


def print_matrix(matrix, title):
    print(f"\n[{title}]")
    for row in matrix:
        print(" ".join(map(str, row)))


# 1. 관계 행렬 입력 기능
def input_relation_matrix():
    print("5x5 관계 행렬을 행 단위로 입력하세요 (0 또는 1, 예: 1 0 0 0 0):")
    matrix = []
    for i in range(N):
        while True:
            raw = input(f"{i + 1}행: ").strip()
            tokens = list(raw) if (len(raw) == N and set(raw) <= {"0", "1"}) else raw.split()
            if len(tokens) == N and all(t in ("0", "1") for t in tokens):
                matrix.append([int(t) for t in tokens])
                break
            print("0 또는 1로 5개 값을 정확히 입력하세요.")
    return matrix


# 2. 동치 관계 판별 기능
def is_reflexive(matrix):
    return all(matrix[i][i] == 1 for i in range(N))


def is_symmetric(matrix):
    return all(matrix[i][j] == matrix[j][i] for i in range(N) for j in range(i + 1, N))


def is_transitive(matrix):
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1:
                for k in range(N):
                    if matrix[j][k] == 1 and matrix[i][k] == 0:
                        return False
    return True


def check_equivalence(matrix):
    r, s, t = is_reflexive(matrix), is_symmetric(matrix), is_transitive(matrix)
    print(f"\n반사: {'O' if r else 'X'}, 대칭: {'O' if s else 'X'}, 추이: {'O' if t else 'X'}")
    if r and s and t:
        print("=> 동치 관계입니다.")
        return r, s, t, True
    print("=> 동치 관계가 아닙니다.")
    return r, s, t, False


# 3. 동치류 출력 기능
def get_equivalence_class(matrix, element):
    idx = SET_A.index(element)
    return [SET_A[j] for j in range(N) if matrix[idx][j] == 1]


def print_equivalence_classes(matrix):
    print("\n[각 원소의 동치류]")
    for elem in SET_A:
        eq_class = get_equivalence_class(matrix, elem)
        print(f"[{elem}] = {{{', '.join(map(str, eq_class))}}}")


# 4. 폐포 구현 기능
def reflexive_closure(matrix):
    res = copy.deepcopy(matrix)
    for i in range(N):
        res[i][i] = 1
    return res


def symmetric_closure(matrix):
    res = copy.deepcopy(matrix)
    for i in range(N):
        for j in range(N):
            if res[i][j] == 1:
                res[j][i] = 1
    return res


def transitive_closure(matrix):
    res = copy.deepcopy(matrix)
    for k in range(N):
        for i in range(N):
            if res[i][k] == 1:
                for j in range(N):
                    if res[k][j] == 1:
                        res[i][j] = 1
    return res


def process_closures(matrix, r, s, t):
    closures = [("반사", r, reflexive_closure), ("대칭", s, symmetric_closure), ("추이", t, transitive_closure)]
    for name, ok, fn in closures:
        if not ok:
            print_matrix(matrix, f"{name} 폐포 변환 전")
            closed = fn(matrix)
            print_matrix(closed, f"{name} 폐포 변환 후")
            _, _, _, is_eq = check_equivalence(closed)
            if is_eq:
                print_equivalence_classes(closed)


# [추가기능] 합성 관계(R◦R) 계산 및 추이 관계·추이 폐포 검증
def compose(m1, m2):
    res = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if m1[i][k] and m2[k][j]:
                    res[i][j] = 1
                    break
    return res


def check_by_composition(matrix):
    r2 = compose(matrix, matrix)
    print_matrix(r2, "추가기능: 합성 관계 R^2 (M ⊙ M)")

    is_trans_r2 = all(not r2[i][j] or matrix[i][j] for i in range(N) for j in range(N))
    print(f"R^2 ⊆ R (추이 관계 판별): {'O' if is_trans_r2 else 'X'}")

    power = copy.deepcopy(matrix)
    r_plus = copy.deepcopy(matrix)
    for _ in range(N - 1):
        power = compose(power, matrix)
        for i in range(N):
            for j in range(N):
                r_plus[i][j] = r_plus[i][j] or power[i][j]

    print_matrix(r_plus, "추가기능: 합성 기반 추이 폐포 R^+ (R ∪ R^2 ∪ ... ∪ R^5)")
    warshall = transitive_closure(matrix)
    print(f"Warshall 추이 폐포와 일치 여부: {'일치 (O)' if r_plus == warshall else '불일치 (X)'}")


def main():
    matrix = input_relation_matrix()
    print_matrix(matrix, "입력된 관계 행렬")
    r, s, t, is_eq = check_equivalence(matrix)
    if is_eq:
        print_equivalence_classes(matrix)
    else:
        process_closures(matrix, r, s, t)

    check_by_composition(matrix)


if __name__ == "__main__":
    main()