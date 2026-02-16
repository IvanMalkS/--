def main():
    print("==========================================")
    print(" ЭКСПЕРТНАЯ СИСТЕМА: ВЫБОР FRONTEND СТЕКА")
    print("==========================================")
    print("Отвечайте на вопросы цифрами (1 или 2)\n")

    # --- ВОПРОС 1: ТИП ПРОЕКТА ---
    print("1. Какой тип проекта разрабатываем?")
    print("   [1] Лендинг / Контентный сайт")
    print("   [2] Веб-приложение (Сервис / SaaS)")
    
    project_type = input("Ваш выбор: ")

    # ВЕТКА 1: ЛЕНДИНГИ
    if project_type == "1":
        # --- ВОПРОС 2 (Для лендингов) ---
        print("\n2. Нужен сложный интерактив (формы, калькуляторы)?")
        print("   [1] Нет (простая визитка)")
        print("   [2] Да (Блог / Документация)")
        
        interactive = input("Ваш выбор: ")

        # ПРАВИЛО 1 (Зн1)
        if interactive == "1":
            print("\n РЕЗУЛЬТАТ: HTML/CSS + Vanilla JS")
        # ПРАВИЛО 2 (Зн2)
        elif interactive == "2":
            print("\n РЕЗУЛЬТАТ: Astro")
        else:
            print("\n Ошибка: Неверный ввод")

    # ВЕТКА 2: ПРИЛОЖЕНИЯ
    elif project_type == "2":
        # --- ВОПРОС 3 (Масштаб) ---
        print("\n2. Масштаб и архитектура проекта?")
        print("   [1] Enterprise / Сложный B2B")
        print("   [2] Startup / SaaS / B2C")
        
        scale = input("Ваш выбор: ")

        # ВЕТКА 2.1: ENTERPRISE
        if scale == "1":
            # --- ВОПРОС 4 (SEO для Enterprise) ---
            print("\n3. Критичен ли SEO / SSR?")
            print("   [1] Да (Публичный портал)")
            print("   [2] Нет (Закрытая CRM)")
            
            seo_ent = input("Ваш выбор: ")

            # ПРАВИЛО 3 (Зн3)
            if seo_ent == "1":
                print("\n РЕЗУЛЬТАТ: Angular + Universal (SSR)")
            # ПРАВИЛО 4 (Зн4)
            elif seo_ent == "2":
                print("\n РЕЗУЛЬТАТ: Angular SPA")
            else:
                print("\n Ошибка: Неверный ввод")

        # ВЕТКА 2.2: STARTUP
        elif scale == "2":
            # --- ВОПРОС 5 (SEO для Startup) ---
            print("\n3. Критичен ли SEO / SSR?")
            print("   [1] Да (Магазин, СМИ)")
            print("   [2] Нет (SPA / Dashboard)")
            
            seo_startup = input("Ваш выбор: ")

            if seo_startup == "1":
                # --- ВОПРОС 6 (Стек команды) ---
                print("\n4. Какой стек ближе команде?")
                print("   [1] React экосистема")
                print("   [2] Vue экосистема")
                
                team = input("Ваш выбор: ")

                # ПРАВИЛО 5 (Зн5)
                if team == "1":
                    print("\n РЕЗУЛЬТАТ: Next.js")
                # ПРАВИЛО 6 (Зн6)
                elif team == "2":
                    print("\n РЕЗУЛЬТАТ: Nuxt")
                else:
                    print("\n Ошибка: Неверный ввод")

            elif seo_startup == "2":
                # --- ВОПРОС 7 (Приоритет) ---
                print("\n4. Что важнее в разработке?")
                print("   [1] Экосистема и легкий найм")
                print("   [2] Скорость разработки и DX")
                
                priority = input("Ваш выбор: ")

                # ПРАВИЛО 7 (Зн7)
                if priority == "1":
                    print("\n РЕЗУЛЬТАТ: Vite + React")
                # ПРАВИЛО 8 (Зн8)
                elif priority == "2":
                    print("\n РЕЗУЛЬТАТ: Vue 3 / Svelte")
                else:
                    print("\n Ошибка: Неверный ввод")
            else:
                print("\n Ошибка: Неверный ввод")
        else:
            print("\n Ошибка: Неверный ввод")
    else:
        print("\n Ошибка: Неверный ввод")

    input("\nНажмите Enter, чтобы выйти...")

if __name__ == "__main__":
    while True:
        main()
        print("\n" + "-"*30 + "\n")