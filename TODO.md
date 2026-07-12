## Backlog

- [x] Пофиксить отображение сайта на мобильных устройствах:
    - [x] Увеличить размер кнопки
    - [x] Починить верстку при горизонтальной ориентации
- [x] Решить вопрос с повторением цитат
- [x] Создать алгоритм для выбора фонового изображения
- [x] Облегчить фоновые изображения
- [x] Попробовать протестировать сайт на производительность
---
- [ ] Перейти на SPA с простой перезагрузки:
  - [ ] Изменить get_next_background, чтобы он выдавал следующее изображение: просто добавить новое условие при % 5 == 1 и вывод двух словарей ссылок
---
- [ ] Подключить Яндекс.Метрику или Google Metrics
## Statistics

Отчет от 9 июля после перехода на Cloudinary от PageSpeed Insights:

Данные из теста для мобильных устройств:
- First Contentful Paint: 2,7с
- Largest Contentful Paint: Error! NO_LCP
- Total Blocking Time: Error! NO_LCP
- Cumulative Layout Shift: 0
- Speed Index: 4,9 сек

Для пк:
- First Contentful Paint: 0,7с
- Largest Contentful Paint: Error! NO_LCP 
- Total Blocking Time: Error! NO_LCP
- Cumulative Layout Shift: 0
- Speed Index: 2,4 сек.

---

Отчет от 6 июля от PageSpeed Insights:

Мобильные устройства:
- First Contentful Paint: 2,7 с
- Largest Contentful Paint: Error! NO_LCP
- Total Blocking Time: Error! NO_LCP
- Speed Index: 4 c

Компьютер: 
- First Contentful Paint: 0,7 с
- Largest Contentful Paint: 0,7 с
- Total Blocking Time: 0 мс
- Speed Index: 1,7 с