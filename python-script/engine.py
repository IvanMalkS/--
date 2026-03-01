import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Sequence = collections.abc.Sequence
    collections.Iterable = collections.abc.Iterable

from experta import *

class ProjectSpecs(Fact):
    """Входные данные (ответы пользователя на 15 факторов)"""
    pass

class FrontendExpert(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.recommendations = []
        self.logs = []
        
        self.scores = {
            'React Native': 0, 
            'Angular': 0, 
            'Next.js': 0, 
            'Nuxt.js': 0, 
            'Astro': 0, 
            'Vue/React SPA': 0
        }
        self.reasons = {stack: [] for stack in self.scores}

    def add_score(self, stack, points, reason):
        if stack in self.scores:
            self.scores[stack] += points
            self.reasons[stack].append(reason)
            self._log(f"Начислено {points} баллов -> {stack}: {reason}")

    def _log(self, text):
        self.logs.append(text)
        print(f"[ЛОГ] {text}")

    # ==========================================
    # УРОВЕНЬ 1: АГРЕГАЦИЯ БАЗОВЫХ ФАКТОРОВ
    # ==========================================

    @Rule(OR(ProjectSpecs(q_region='world'), ProjectSpecs(q_env='transport')))
    def net_bad(self):
        self.declare(Fact(net_qual='bad'))
        self._log("Качество сети: Плохое (Широкая гео-зона ИЛИ мобильная среда)")

    @Rule(AND(ProjectSpecs(q_region='region'), ProjectSpecs(q_env='office')))
    def net_good(self):
        self.declare(Fact(net_qual='good'))
        self._log("Качество сети: Хорошее (Локальный регион И офис/дом)")

    @Rule(OR(ProjectSpecs(q_size='small'), ProjectSpecs(q_exp='no_senior')))
    def team_weak(self):
        self.declare(Fact(team_cap='weak'))
        self._log("Сила команды: Слабая (Мало людей ИЛИ нет Senior-разработчиков)")

    @Rule(AND(ProjectSpecs(q_size='large'), ProjectSpecs(q_exp='has_senior')))
    def team_strong(self):
        self.declare(Fact(team_cap='strong'))
        self._log("Сила команды: Сильная (Достаточная команда И есть опыт)")

    # ==========================================
    # УРОВЕНЬ 2: ФОРМИРОВАНИЕ ПРОМЕЖУТОЧНЫХ УЗЛОВ (РИСК И МОЩНОСТЬ)
    # ==========================================

    @Rule(OR(Fact(net_qual='bad'), ProjectSpecs(q_dev='phone')))
    def client_weak(self):
        self.declare(Fact(client_pow='weak'))
        self._log("Мощность клиента: Слабая (Плохая сеть ИЛИ мобильные устройства)")

    @Rule(AND(Fact(net_qual='good'), ProjectSpecs(q_dev='pc')))
    def client_strong(self):
        self.declare(Fact(client_pow='strong'))
        self._log("Мощность клиента: Сильная (Хорошая сеть И десктоп)")

    @Rule(Fact(team_cap='weak'))
    def risk_high(self):
        self.declare(Fact(risk_calc='high'))
        self._log("Риск-профиль: Высокий (Обусловлено слабой командой)")

    @Rule(Fact(team_cap='strong'))
    def risk_low(self):
        self.declare(Fact(risk_calc='low'))
        self._log("Риск-профиль: Низкий (Обусловлено сильной командой)")

    # ==========================================
    # УРОВЕНЬ 3: ТЯЖЕСТЬ САЙТА И КУЛЬТУРА РАЗРАБОТКИ
    # ==========================================

    @Rule(OR(Fact(client_pow='weak'), ProjectSpecs(q_content='video')))
    def perf_critical(self):
        self.declare(Fact(perf_calc='critical'))
        self._log("Тяжесть сайта: Критическая (Слабый клиент ИЛИ тяжелый контент)")

    @Rule(AND(Fact(client_pow='strong'), ProjectSpecs(q_content='text')))
    def perf_normal(self):
        self.declare(Fact(perf_calc='normal'))
        self._log("Тяжесть сайта: Норма (Десктоп и легкий текстовый контент)")

    @Rule(OR(Fact(risk_calc='high'), ProjectSpecs(q_time='urgent')))
    def culture_fast(self):
        self.declare(Fact(culture='fast'))
        self._log("Культура: Быстро / MVP (Горят сроки ИЛИ высокие риски)")

    @Rule(AND(Fact(risk_calc='low'), ProjectSpecs(q_time='time')))
    def culture_reliable(self):
        self.declare(Fact(culture='reliable'))
        self._log("Культура: Надежно / Enterprise (Есть время и ресурсы)")

    @Rule(ProjectSpecs(q_ts='yes'))
    def bonus_typescript(self):
        self.add_score("Angular", 25, "TypeScript: Angular принудительно и повсеместно использует строгую статическую типизацию. Это кардинально снижает шанс возникновения багов в бизнес-логике, что критически важно для надежности.")
        self.add_score("Next.js", 15, "TypeScript: Next.js имеет первоклассную (first-class) поддержку TypeScript 'из коробки'. Связка React + Typescript является стандартом индустрии для создания веб-интерфейсов.")
        self.add_score("Nuxt.js", 15, "TypeScript: Начиная с 3-й версии, ядро Nuxt.js полностью переписано на TypeScript, что обеспечивает 100% типизацию встроенных плагинов и удобство API.")

    # ==========================================
    # УРОВЕНЬ 4: ОПРЕДЕЛЕНИЕ СТОЛПОВ АРХИТЕКТУРЫ
    # ==========================================

    # 4.1. Способ рендеринга
    @Rule(AND(Fact(perf_calc='critical'), ProjectSpecs(q_seo='yes')))
    def render_ssg(self):
        self.declare(Fact(render='SSG'))
        self._log("Выбран паттерн: SSG (Нужно SEO + Критическая производительность)")

    @Rule(AND(Fact(perf_calc='normal'), ProjectSpecs(q_seo='yes')))
    def render_ssr(self):
        self.declare(Fact(render='SSR'))
        self._log("Выбран паттерн: SSR (Нужно SEO + Нормальная производительность)")

    @Rule(ProjectSpecs(q_seo='no'))
    def render_spa(self):
        self.declare(Fact(render='SPA'))
        self._log("Выбран паттерн: SPA (SEO не требуется)")

    # 4.2. Мобильность
    @Rule(OR(ProjectSpecs(q_store='no'), AND(ProjectSpecs(q_store='yes'), ProjectSpecs(native_req='no'))))
    def mobile_web(self):
        self.declare(Fact(mobile='Web'))
        self._log("Мобильность: Web-приложение")

    @Rule(AND(ProjectSpecs(q_store='yes'), ProjectSpecs(native_req='yes')))
    def mobile_native(self):
        self.declare(Fact(mobile='Native'))
        self._log("Мобильность: Нативное мобильное приложение")

    # 4.3. UI (Дизайн)
    @Rule(ProjectSpecs(q_lib='no'))
    def ui_kit(self):
        self.declare(Fact(ui='UI-Kit'))
        self._log("UI: Нет своего дизайна, используем готовые компоненты (UI-Kit)")

    @Rule(ProjectSpecs(q_lib='yes'))
    def ui_custom(self):
        self.declare(Fact(ui='Custom'))
        self._log("UI: Есть готовый дизайн, реализуем его (Custom)")

    # 4.4. State (Состояние)
    @Rule(OR(ProjectSpecs(q_real='yes'), ProjectSpecs(q_offline='yes')))
    def state_complex(self):
        self.declare(Fact(state='Complex'))
        self._log("State: Сложный стейт-менеджмент (Realtime чат ИЛИ Offline работа)")
    
    @Rule(AND(ProjectSpecs(q_real='no'), ProjectSpecs(q_offline='no')))
    def state_simple(self):
        self.declare(Fact(state='Simple'))
        self._log("State: Простой стейт")

    # 4.5. Infra (Инфраструктура)
    @Rule(OR(ProjectSpecs(q_host='little'), ProjectSpecs(q_traffic='yes')))
    def infra_cloud(self):
        self.declare(Fact(infra='Cloud'))
        self._log("Infra: Ограниченный бюджет ИЛИ скачки трафика -> Cloud/Serverless")
        
    @Rule(AND(ProjectSpecs(q_host='much'), ProjectSpecs(q_traffic='no')))
    def infra_own(self):
        self.declare(Fact(infra='Own'))
        self._log("Infra: Достаточный бюджет И стабильный трафик -> Own servers")

    # ==========================================
    # УРОВЕНЬ 5: ИТОГОВЫЙ ВЫВОД СТЕКА (Балльная система)
    # ==========================================

    @Rule(Fact(mobile='Native'), salience=100)
    def rec_react_native(self):
        self.add_score("React Native", 100, "Кроссплатформенная мобильная разработка: Вы указали строгую необходимость публикации приложения в AppStore/Google Play и потребность в доступе к нативным функциям устройства (камера, геолокация, контакты). React Native является оптимальным выбором: он позволяет писать единую кодовую базу для iOS и Android, предоставляя при этом прямой мост к нативному API телефона.")

    @Rule(AND(Fact(mobile='Web'), Fact(culture='reliable'), OR(Fact(render='SSR'), Fact(render='SSG'))))
    def rec_angular_ssr(self):
        self.add_score("Angular", 40, "Крупный Enterprise-проект с SEO: Вашему Web-сервису требуется отличная индексация поисковиками (SEO), сильная команда и упор на долгосрочную поддержку (культура 'Надежно'). Современный Angular предоставляет мощный встроенный механизм серверного рендеринга (SSR), а его архитектура надежно защищает проект от хаоса при росте кодовой базы.")

    @Rule(AND(Fact(mobile='Web'), Fact(culture='reliable'), Fact(render='SPA')))
    def rec_angular_spa(self):
        self.add_score("Angular", 40, "Сложная внутренняя система (SPA): Проекту не требуется SEO, это, вероятно, корпоративная CRM, ERP или дашборд. Учитывая приоритет 'Надежно', вам нужны строгие стандарты разработки. Angular 'из коробки' заставляет команду писать предсказуемый код, благодаря чему отлично масштабируется на сложных бизнес-задачах.")

    @Rule(AND(Fact(mobile='Web'), Fact(culture='fast'), Fact(render='SPA')))
    def rec_vue_spa(self):
        self.add_score("Vue/React SPA", 40, "Быстрый запуск (SPA): Проекту не нужно SEO, но ключевым фактором является скорость разработки и гибкость. Использование Vue или React в формате Single Page Application (со сборщиком Vite) позволит вашей команде максимально быстро проверить гипотезу, запустить продукт и легко найти новых разработчиков для поддержки.")

    @Rule(AND(Fact(mobile='Web'), Fact(render='SSG'), Fact(perf_calc='critical')))
    def rec_astro(self):
        self.add_score("Astro", 40, "Контентный проект с критической производительностью: Одной из ваших главных целей является SEO и максимальная производительность сайта (что важно из-за слабых сетей устройств аудитории или тяжелого медиа-контента). Уникальная архитектура 'Island' от Astro отдаст пользователю чистый HTML, загружая JS только там, где это абсолютно необходимо.")

    @Rule(AND(Fact(mobile='Web'), Fact(team_cap='strong'), OR(Fact(render='SSR'), Fact(render='SSG'))))
    def rec_next(self):
        self.add_score("Next.js", 30, "Масштабный портал с SEO: Вам требуется продвижение в поиске (через SSR/SSG), и у вас сильная команда. Next.js сегодня — это мощный индустриальный стандарт в экосистеме React для создания масштабных порталов и e-commerce проектов.")

    @Rule(AND(Fact(mobile='Web'), Fact(team_cap='weak'), OR(Fact(render='SSR'), Fact(render='SSG'))))
    def rec_nuxt(self):
        self.add_score("Nuxt.js", 30, "SEO-портал для небольшой команды: Проекту необходимо SEO, но у вас нет большой команды с сильной Senior-экспертизой. Nuxt.js (база Vue) славится великолепным Developer Experience: он берет на себя много сложных архитектурных решений под капотом и прощает многие ошибки новичков.")


    @Rule(Fact(ui='UI-Kit'))
    def bonus_ui(self):
        self.add_score("Next.js", 15, "UI: Учитывая отсутствие готового дизайна, в Next.js (React) доступна гигантская база компонентов (MUI, Radix, Tailwind UI), что ускорит сборку интерфейсов.")
        self.add_score("Angular", 15, "UI: Angular Material — это превосходное, монолитное решение для построения строгих систем из надежных и протестированных готовых компонентов.")
        self.add_score("Vue/React SPA", 15, "UI: У SPA на React/Vue самая большая экосистема библиотек, позволяющая собрать интерфейс как конструктор без привлечения дизайнеров.")

    @Rule(Fact(state='Complex'))
    def bonus_state(self):
        self.add_score("Angular", 20, "State: Т.к. есть сложные потоки данных или чаты в реальном времени, встроенная в Angular библиотека RxJS дает невероятно мощные возможности для работы с асинхронностью без костылей.")
        self.add_score("Vue/React SPA", 20, "State: Экосистема React/Vue использует проверенные инструменты стейт-менеджмента (Redux, Zustand, Pinia), которые отлично подходят для сложной масштабируемой логики клиента.")
        self.add_score("Next.js", 15, "State: React имеет богатейший встроенный и сторонний инструментарий (Hooks, Context) для стабильного управления сложным состоянием.")

    @Rule(Fact(infra='Cloud'))
    def bonus_infra_cloud(self):
        self.add_score("Next.js", 25, "Infra: Ваш трафик скачет. Next.js разрабатывается создателями Vercel, поэтому он идеально деплоится на serverless/cloud инфраструктуру (выдерживая любые нагрузки).")
        self.add_score("Nuxt.js", 25, "Infra: Ядро Nitro в Nuxt.js изначально создано с прицелом на легкое бессерверное, cloud-native развертывание (Edge Functions) для обработки скачков трафика.")
        self.add_score("Astro", 10, "Infra: Статические страницы Astro максимально дешево и легко развертываются/кэшируются на любом CDN по всему миру.")

    @Rule(Fact(render='SSG'))
    def bonus_render_ssg(self):
        self.add_score("Astro", 20, "Рендер: Для чисто статических сайтов Astro является абсолютным лидером, генерируя 'легкий' HTML без излишков JavaScript.")
        self.add_score("Next.js", 15, "Рендер: Next.js имеет встроенную и гибко настраиваемую генерацию ISR (Incremental Static Regeneration).")
        self.add_score("Angular", 15, "Рендер: Angular поддерживает пререндеринг страниц в HTML через механизм Angular Universal.")     

    @Rule(Fact(culture='reliable'))
    def penalty_astro_enterprise(self):
        self.add_score("Astro", -20, "Enterprise-архитектура: Astro создан больше для контентных сайтов. Его архитектура островов (Island) не так оптимальна для сложных корпоративных систем по сравнению со строгими JS/TS-фреймворками (Angular/Nest.js).")

    def get_final_recommendation(self):
        sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        valid_scores = [(stack, score) for stack, score in sorted_scores if score > 0]
        top_stacks = valid_scores[:3]
        
        self.recommendations = []
        print("\n" + "="*46)
        print(" ИТОГОВЫЙ РЕЙТИНГ ТЕХНОЛОГИЙ (ТОП):")
        print("="*46)

        for stack, score in top_stacks:
            reasons_txt = "\n".join(f"- {r}" for r in self.reasons[stack])
            reason = f"Общий балл: {score}\nОбоснование:\n{reasons_txt}\n"
            self.recommendations.append({"stack": stack, "reason": reason})
            
            print(f"\n[{stack}] — ({score} баллов)")
            print(f"{reasons_txt}")
