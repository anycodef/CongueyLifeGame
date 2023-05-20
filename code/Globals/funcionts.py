def is_on_top_of(rect, pos) -> bool:
    return rect.x <= pos[0] <= rect.x + rect.width and rect.y <= pos[1] <= rect.y + rect.height


def greatest_common_divisor(a, b):
    a, b = int(a), int(b)

    mcd = a
    if b < a:
        mcd = b

    while a % mcd != 0 or b % mcd != 0:
        mcd -= 1

    return mcd



