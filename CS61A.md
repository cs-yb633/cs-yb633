# CS61A

## Week 4

### hw03：Recursion and Recurision tree

>==**递归树**==: 一个函数调用自己，产生更小规模的子问题。
>
>* **整数拆分** 分为调用目前最大值和不调用目前最大值两种情况 加在一起便是其全部情况

####  **凑钱问题**

```py
def next_smaller_dollar(bill):
    """Returns the next smaller bill in order."""
    if bill == 100:
        return 50
    if bill == 50:
        return 20
    if bill == 20:
        return 10
    elif bill == 10:
        return 5
    elif bill == 5:
        return 1
    
def count_dollars(total):
        """Return the number of ways to make change.

    >>> count_dollars(15)  # 15 $1 bills, 10 $1 & 1 $5 bills, ... 1 $5 & 1 $10 bills
    6
    >>> count_dollars(10)  # 10 $1 bills, 5 $1 & 1 $5 bills, 2 $5 bills, 10 $1 bills
    4
    >>> count_dollars(20)  # 20 $1 bills, 15 $1 & $5 bills, ... 1 $20 bill
    10
    >>> count_dollars(45)  # How many ways to make change for 45 dollars?
    44
    >>> count_dollars(100) # How many ways to make change for 100 dollars?
    344
    >>> count_dollars(200) # How many ways to make change for 200 dollars?
    3274
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(SOURCE_FILE, 'count_dollars', ['While', 'For'])
    True
    """
        "*** YOUR CODE HERE ***"
        def constrained_count(total, largest_bill):
            if total == 0:
                return 1
            if total < 0:
                return 0
            if largest_bill == None:
                return 0
            without_dollar_bill = constrained_count(total, next_smaller_dollar(largest_bill))
            with_dollar_bill = constrained_count(total - largest_bill, largest_bill)
            return without_dollar_bill + with_dollar_bill
        return constrained_count(total, 100)
```

> 如上的凑钱问题与整数分解如出一辙

---



#### **汉诺塔问题**

在汉诺塔游戏中，有 **三根柱子** 和若干个 **不同大小的盘子**。盘子最初按照大小顺序堆叠在一根柱子上，最小的盘子在最顶层，最大的盘子在最底层。

目标是将所有盘子从 **起始柱**（起始杆）移动到 **目标柱**（目标杆），遵循以下的规则。

1. **一次只能移动一个盘子。**
	 每次只能移动柱子上最上面（也就是最小）的盘子。
2. **每次移动必须将盘子从一个柱子移动到另一个柱子。**
	 你只能把盘子从一个柱子拿起来，移动到另一柱子上。
3. **不能把大盘子放到小盘子上面。**
	 每次移动盘子时，必须保证目标柱上的盘子按照从大到小的顺序排列。换句话说，大盘子永远不能在小盘子上面。
4. **最终目标：**
	 将所有盘子从 **起始柱** 移动到 **目标柱**，同时满足上述规则。

代码实现：

```python
def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)

def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    "*** YOUR CODE HERE ***"
    if n==1:
        print_move(start,end)
    else:
        move_stack(n-1,start,6-start-end)    
        print_move(start,end)
        move_stack(n-1,6-start-end,end)
```

>通过这个问题 理解到
>
>**递归 = 找到一个问题的自相似结构（大问题由更小的同类问题构成），并利用小问题的答案来组合成大问题的答案，直到最终缩到无法再缩的基本情况。**
>
>~~并不需要分析复杂问题的各种情况~~

---

#### 无名递归

在这一题中，你需要写出一个 **没有名字** 的 **递归函数**。
 你不能使用：

- `def`
- 任何赋值（`=`）
- 任何形式的给函数起名字
- 不能出现直接递归的函数调用（例如 `fact(n-1)`）

然而你需要实现：

```
make_anonymous_factorial()(n)
```

的值等于 `n!`

代码实现：

```py
from operator import sub, mul

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> # ban any assignments or recursion
    >>> check(SOURCE_FILE, 'make_anonymous_factorial',
    ...     ['Assign', 'AnnAssign', 'AugAssign', 'NamedExpr', 'FunctionDef', 'Recursion'])
    True
    """
    return (lambda f: f(f))(lambda f: lambda x: 1 if x == 0 else x * f(f)(x - 1))

```



- **第一个 `()` 是给外层函数传参数，用来填入 maker（或 f）**
- **第二个 `(5)` 是给内层返回的函数传参数，也就是 n**

换句话说：

```python
make_anonymous_factorial()
            ↑   给外层函数传参数（maker / f）
make_anonymous_factorial()(5)
                        ↑  给内层函数传参数（n）
```

---



## Week5

### lab03: Recursion, Python Lists

#### Q6: Squares Only

> Implement the function `squares`, which takes in a list of positive integers. It returns a list that contains the square roots of the elements of the original list that are perfect squares. Use a list comprehension.

**错误代码**

```py
def squares(s: list[int]) -> list[int]:
    """Returns a new list containing square roots of the elements of the
    original list that are perfect squares.

    >>> seq = [8, 49, 8, 9, 2, 1, 100, 102]
    >>> squares(seq)
    [7, 3, 1, 10]
    >>> seq = [500, 30]
    >>> squares(seq)
    []
    """
    return [sqrt(n) for n in s if isinstance(sqrt(n),int)]
```

**错误原因：sqrt（）是数学函数 自然返回float 故应改变sqrt类型后用round（）函数**

**改正后：**

```py
def squares(s: list[int]) -> list[int]:
    """Returns a new list containing square roots of the elements of the
    original list that are perfect squares.

    >>> seq = [8, 49, 8, 9, 2, 1, 100, 102]
    >>> squares(seq)
    [7, 3, 1, 10]
    >>> seq = [500, 30]
    >>> squares(seq)
    []
    """
    return [int(sqrt(n)) for n in s if sqrt(n)==round(sqrt(n))]

```

---

#### Q8: Making Onions

> Write a function `make_onion` that takes in two one-argument functions, `f` and `g`. It returns a function that takes in three arguments: `x`, `y`, and `limit`. The returned function returns `True` if it is possible to reach `y` from `x` using up to `limit` calls to `f` and `g`, and `False` otherwise.

For example, if `f` adds 1 and `g` doubles, then it is possible to reach 25 from 5 in four calls: `f(g(g(f(5))))`.

```py
def make_onion(f, g):
    """Return a function can_reach(x, y, limit) that returns
    whether some call expression containing only f, g, and x with
    up to limit calls will give the result y.

    >>> up = lambda x: x + 1
    >>> double = lambda y: y * 2
    >>> can_reach = make_onion(up, double)
    >>> can_reach(5, 25, 4)      # 25 = up(double(double(up(5))))
    True
    >>> can_reach(5, 25, 3)      # Not possible
    False
    >>> can_reach(1, 1, 0)      # 1 = 1
    True
    >>> add_ing = lambda x: x + "ing"
    >>> add_end = lambda y: y + "end"
    >>> can_reach_string = make_onion(add_ing, add_end)
    >>> can_reach_string("cry", "crying", 1)      # "crying" = add_ing("cry")
    True
    >>> can_reach_string("un", "unending", 3)     # "unending" = add_ing(add_end("un"))
    True
    >>> can_reach_string("peach", "folding", 4)   # Not possible
    False
    """
    def can_reach(x, y, limit):
        if limit < 0:
            return False
        elif x == y:
            return True
        else:
            return can_reach(f(x), y, limit - 1) or can_reach(g(x), y, limit - 1)
    return can_reach
```

> 
>
> **or的机制：并非一般的布尔或，若第一个表达式为真则返回第一个 若第一个为假则无论第二个真假均返回第二个表达式**

---

#### Q9: Ten-Pairs

Write a function that takes a positive integer `n` and returns the number of ten-pairs it contains. A ten-pair is a pair of digits within `n` that sums to 10.

The number 7,823,952 has 3 ten-pairs. The first and fourth digits sum to 7+3=10, the second and third digits sum to 8+2=10, and the second and last digit sum to 8+2=10.

Important notes:

- A digit can be part of more than one ten-pair.
- One 5 does not make a ten-pair with itself.

> *Recommended*: Complete and use the helper function `count_digit` to calculate how many times a digit appears in `n`.

**Important:** Use recursion; the tests will fail if you use any loops (for, while).

**听从建议构造辅助函数代码：**

```py
def ten_pairs(n):
    """Return the number of ten-pairs within positive integer n.

    >>> ten_pairs(7823952) # 7+3, 8+2, and 8+2
    3
    >>> ten_pairs(55055)
    6
    >>> ten_pairs(9641469) # 9+1, 6+4, 6+4, 4+6, 1+9, 4+6 
    6
    >>> # ban iteration
    >>> from construct_check import check
    >>> check(SOURCE_FILE, 'ten_pairs', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    if n == 0 :
        return 0
    else:
        return ten_pairs(n//10)+count_digit(n//10,10-n%10)
   
    

def count_digit(n, digit):
    """Return how many times digit appears in n.

    >>> count_digit(55055, 5) # digit 5 appears 4 times in 55055
    4
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(SOURCE_FILE, 'count_digits', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    if n == 0 :
        return 0
    elif n%10 == digit:
        return count_digit(n//10,digit)+1
    else:return count_digit(n//10,digit)

```

> 实现目标函数的代码非常简洁，思路清晰

**仅使用ten_pairs()代码：**

```py
def ten_pairs(n):

    if n < 10:
        return 0

    last = n % 10          # 固定当前 digit
    rest = n // 10         # 剩余部分

    # 内部递归：统计 rest 中有多少个数字与 last 配对成 10
    def count_pairs(x):
        if x == 0:
            return 0
        return (1 if x % 10 + last == 10 else 0) + count_pairs(x // 10)

    # 总数 =（rest 中与 last 配对的数量）+ （递归处理 rest 的 ten_pairs）
    return count_pairs(rest) + ten_pairs(rest)

```

> 递归树做法 较推荐做法复杂 思路简单
>
> * 最外层固定 **n 的最后一位 digit1 = n % 10**
>
> * 内层函数 **digit(x)** 去遍历 n 的剩余部分（即 x=n//10）
>
> * 如果出现 x%10 + digit1 == 10 就计数
>
> * 然后再递归到下一位
>
> 	---





​	

​	