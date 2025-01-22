
# Dustman game

Очередная примитивная игра. Идея: игрок перемещается по карте, на которой разбросан мусор и есть корзины для этого мусора. Игрок может собирать мусор и класть его в корзины. По мере прохождения, повышается уровень игрока: он может подбирать больше мусора. Есть еще идеи дальнейших модификаций...   

Пока консольный вариант, на стадии разработки. Реализована базовая механика, позже прикручу PyGame.

```
 -=--=--=--=--=--=--=--=--=--=-
|                   t  t     b | 0
|       d        b             | 1
|             t              t | 2
| t              t             | 3
|                              | 4
|       t     t        b       | 5
|                              | 6
|    b  t                      | 7
|                              | 8
|             t  b             | 9
 -=--=--=--=--=--=--=--=--=--=-
  0  1  2  3  4  5  6  7  8  9
```

d - игрок (dustman)  
t - мусор (trash)  
b - корзина (bin)  

Управление (нажимаем клавишу соответствующего символа и Enter):  
s - влево  
f - вправо  
e - вверх  
d - вниз  
a - подобрать мусор (нужно находиться на мусоре)  
r - сбросить мусор в корзину (нужно находиться на корзине)  
q - выход из игры
