import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Sequence = collections.abc.Sequence
    collections.Iterable = collections.abc.Iterable

from experta import *

class ProjectSpecs(Fact):
    """Входные данные (ответы пользователя)"""
    pass

class FrontendExpert(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.recommendations = []

    # ==========================================
    # УРОВЕНЬ 2: ПЕРВИЧНЫЕ СЛИЯНИЯ (Система вычисляет сама)
    # ==========================================

    # 1. Вычисление качества сети (NET_QUAL)
    @Rule(OR(ProjectSpecs(region='2'), ProjectSpecs(env='2')))
    def net_bad(self):
        self.declare(Fact(net_qual='bad'))
        print(": Вычисляю качество сети... -> ПЛОХОЕ (Влияет удаленный регион или мобильная среда)")

    @Rule(AND(ProjectSpecs(region='1'), ProjectSpecs(env='1')))
    def net_good(self):
        self.declare(Fact(net_qual='good'))
        print(": Вычисляю качество сети... -> ХОРОШЕЕ (Локальный сервер и стационарная среда)")

    # 2. Вычисление силы команды (TEAM_CAP)
    @Rule(OR(ProjectSpecs(team_size='2'), ProjectSpecs(team_exp='2')))
    def team_weak(self):
        self.declare(Fact(team_cap='weak'))
        print(": Оцениваю емкость команды... -> НИЗКАЯ (Нехватка людей или опыта)")

    @Rule(AND(ProjectSpecs(team_size='1'), ProjectSpecs(team_exp='1')))
    def team_strong(self):
        self.declare(Fact(team_cap='strong'))
        print(": Оцениваю емкость команды... -> ВЫСОКАЯ (Большая опытная команда)")

    # ==========================================
    # УРОВЕНЬ 3 и 4: СЛОЖНЫЕ ВЫЧИСЛЕНИЯ (Промежуточные слои)
    # ==========================================

    # 3. Возможности пользователя (CLIENT_POW)
    @Rule(AND(Fact(net_qual='bad'), ProjectSpecs(device='1')))
    def client_weak(self):
        self.declare(Fact(client_pow='weak'))
        print(": Слияние (Сеть + Устройство) -> МОЩНОСТЬ КЛИЕНТА СЛАБАЯ")

    @Rule(OR(Fact(net_qual='good'), ProjectSpecs(device='2')))
    def client_strong(self):
        self.declare(Fact(client_pow='strong'))
        print(": Слияние (Сеть + Устройство) -> МОЩНОСТЬ КЛИЕНТА ВЫСОКАЯ")

    # 4. Допустимая тяжесть сайта (PERF_CALC)
    @Rule(OR(Fact(client_pow='weak'), ProjectSpecs(content_heavy='1')))
    def perf_light(self):
        self.declare(Fact(perf_calc='light'))
        print(": Анализ производительности -> ТРЕБУЕТСЯ ЛЕГКИЙ САЙТ (Жесткий бюджет JS)")

    @Rule(AND(Fact(client_pow='strong'), ProjectSpecs(content_heavy='2')))
    def perf_heavy(self):
        self.declare(Fact(perf_calc='heavy'))
        print(": Анализ производительности -> ДОПУСТИМ ТЯЖЕЛЫЙ САЙТ")

    # 5. Право на ошибку / Культура (RISK_CALC -> CULTURE)
    @Rule(AND(Fact(team_cap='weak'), ProjectSpecs(deadline='1')))
    def culture_fast(self):
        self.declare(Fact(culture='fast'))
        print(": Анализ рисков -> ВЫБРАН ПОДХОД MVP (Сроки горят, ресурсов мало)")

    @Rule(OR(Fact(team_cap='strong'), ProjectSpecs(deadline='2')))
    def culture_strict(self):
        self.declare(Fact(culture='strict'))
        print(": Анализ рисков -> ВЫБРАНА СТРОГАЯ АРХИТЕКТУРА (Есть ресурсы и время)")

    # ==========================================
    # УРОВЕНЬ 5: 6 ФИНАЛЬНЫХ СТОЛПОВ
    # ==========================================

    # СТОЛП 1: Рендеринг (RENDER_MODE)
    @Rule(AND(Fact(perf_calc='light'), ProjectSpecs(seo='1')))
    def render_ssg(self): self.declare(Fact(render_mode='SSG'))
    
    @Rule(AND(Fact(perf_calc='heavy'), ProjectSpecs(seo='1')))
    def render_ssr(self): self.declare(Fact(render_mode='SSR'))
    
    @Rule(ProjectSpecs(seo='2'))
    def render_spa(self): self.declare(Fact(render_mode='SPA'))

    # СТОЛП 2: Данные (STATE_ARCH)
    @Rule(OR(ProjectSpecs(real_time='1'), ProjectSpecs(offline='1')))
    def state_complex(self): self.declare(Fact(state_arch='Complex'))
    
    @Rule(AND(ProjectSpecs(real_time='2'), ProjectSpecs(offline='2')))
    def state_simple(self): self.declare(Fact(state_arch='Simple'))

    # СТОЛП 3: Инфраструктура (INFRA_TYPE)
    @Rule(AND(ProjectSpecs(budget='2'), ProjectSpecs(traffic='1')))
    def infra_serverless(self): self.declare(Fact(infra_type='Serverless'))
    
    @Rule(OR(ProjectSpecs(budget='1'), ProjectSpecs(traffic='2')))
    def infra_server(self): self.declare(Fact(infra_type='Server'))

    # СТОЛП 4: Дизайн (UI_PATTERN)
    @Rule(AND(ProjectSpecs(design='1'), ProjectSpecs(anim='2')))
    def ui_template(self): self.declare(Fact(ui_pattern='Template'))
    
    @Rule(OR(ProjectSpecs(design='2'), ProjectSpecs(anim='1')))
    def ui_custom(self): self.declare(Fact(ui_pattern='Custom'))

    # СТОЛП 5: Мобильность (MOBILE_STRAT) - Пропускаемая ветка
    @Rule(ProjectSpecs(is_mobile='2'))
    def mobile_web(self): self.declare(Fact(mobile_strat='Web_Only'))
    
    @Rule(AND(ProjectSpecs(is_mobile='1'), ProjectSpecs(native_req='2')))
    def mobile_pwa(self): self.declare(Fact(mobile_strat='PWA'))
    
    @Rule(AND(ProjectSpecs(is_mobile='1'), ProjectSpecs(native_req='1')))
    def mobile_native(self): self.declare(Fact(mobile_strat='Native'))

    # ==========================================
    # УРОВЕНЬ 6: ФИНАЛЬНЫЙ СТЕК (Вершина)
    # ==========================================

    @Rule(Fact(mobile_strat='Native'))
    def rec_react_native(self):
        self._print_result("REACT NATIVE + NEXT.JS", "Из-за требования доступа к железу телефона (камера/GPS) нужна нативная разработка.")

    @Rule(AND(Fact(render_mode='SSG'), Fact(mobile_strat='Web_Only')))
    def rec_astro(self):
        self._print_result("ASTRO", "Вам важен SEO, но система выявила слабую мощность клиентов (нужен легкий сайт). Astro отдает HTML без тяжелого JS.")

    @Rule(AND(Fact(culture='strict'), Fact(state_arch='Complex')))
    def rec_angular(self):
        self._print_result("ANGULAR", "Сложная работа с данными и наличие времени/опыта требуют надежного Enterprise-фреймворка со строгим ООП.")

    @Rule(AND(Fact(culture='fast'), Fact(render_mode='SPA')))
    def rec_vue(self):
        self._print_result("VUE.JS / NUXT", "Идеально для быстрой разработки (MVP). Легкий вход, высокая скорость создания интерфейса.")

    @Rule(AND(Fact(infra_type='Serverless'), Fact(render_mode='SSR')))
    def rec_next(self):
        self._print_result("NEXT.JS", "Вам нужно SSR для SEO и готовность к скачкам трафика при малом бюджете на сервера (Serverless Vercel).")

    def _print_result(self, stack, reason):
        self.recommendations.append({"stack": stack, "reason": reason})
        print("\n" + "="*50)
        print(f"РЕКОМЕНДУЕМЫЙ СТЕК ТЕХНОЛОГИЙ: {stack}")
        print(f"Обоснование ЭС: {reason}")
        print("="*50 + "\n")
