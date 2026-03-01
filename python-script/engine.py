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
        self.logs = []

    def _log(self, text):
        self.logs.append(text)
        print(text)

    # ==========================================
    # УРОВЕНЬ 1: КАЧЕСТВО СЕТИ И СИЛА КОМАНДЫ
    # ==========================================

    @Rule(OR(ProjectSpecs(q_region='world'), ProjectSpecs(q_env='transport')))
    def net_bad(self):
        self.declare(Fact(net_qual='bad'))
        self._log("Вычисляю качество сети: Плохое (Широкая гео-зона или мобильная среда)")

    @Rule(AND(ProjectSpecs(q_region='region'), ProjectSpecs(q_env='office')))
    def net_good(self):
        self.declare(Fact(net_qual='good'))
        self._log("Вычисляю качество сети: Хорошее (Локальный регион и домашняя/офисная среда)")

    @Rule(OR(ProjectSpecs(q_size='few'), ProjectSpecs(q_exp='no')))
    def team_weak(self):
        self.declare(Fact(team_cap='weak'))
        self._log("Вычисляю силу команды: Слабая (Нехватка разработчиков или опыта)")

    @Rule(AND(ProjectSpecs(q_size='many'), ProjectSpecs(q_exp='yes')))
    def team_strong(self):
        self.declare(Fact(team_cap='strong'))
        self._log("Вычисляю силу команды: Сильная (Достаточная команда с наличием Senior-разработчиков)")

    # ==========================================
    # УРОВЕНЬ 2: МОЩНОСТЬ КЛИЕНТА И РИСК-ПРОФИЛЬ
    # ==========================================

    @Rule(OR(Fact(net_qual='bad'), ProjectSpecs(q_dev='phone')))
    def client_weak(self):
        self.declare(Fact(client_pow='weak'))
        self._log("Вычисляю мощность клиента: Слабая (Мобильные устройства или плохая сеть)")

    @Rule(AND(Fact(net_qual='good'), ProjectSpecs(q_dev='pc')))
    def client_strong(self):
        self.declare(Fact(client_pow='strong'))
        self._log("Вычисляю мощность клиента: Сильная (Десктоп и хорошая сеть)")

    @Rule(Fact(team_cap='weak'))
    def risk_high(self):
        self.declare(Fact(risk_calc='high'))
        self._log("Риск-профиль: Высокий (Команда со слабым потенциалом)")

    @Rule(Fact(team_cap='strong'))
    def risk_low(self):
        self.declare(Fact(risk_calc='low'))
        self._log("Риск-профиль: Низкий (Сильная опытная команда)")

    # ==========================================
    # УРОВЕНЬ 3: ТЯЖЕСТЬ САЙТА И КУЛЬТУРА
    # ==========================================

    @Rule(OR(Fact(client_pow='weak'), ProjectSpecs(q_content='video')))
    def perf_critical(self):
        self.declare(Fact(perf_calc='critical'))
        self._log("Тяжесть сайта: Критическая (Слабый клиент или тяжелый медиаконтент, нужна максимальная оптимизация)")

    @Rule(AND(Fact(client_pow='strong'), ProjectSpecs(q_content='text')))
    def perf_normal(self):
        self.declare(Fact(perf_calc='normal'))
        self._log("Тяжесть сайта: Норма (Менее строгие требования к производительности)")

    @Rule(OR(Fact(risk_calc='high'), ProjectSpecs(q_time='urgent')))
    def culture_fast(self):
        self.declare(Fact(culture='fast'))
        self._log("Культура: Быстро (Срочность или высокие риски обязывают выбрать MVP или быстрый путь)")

    @Rule(AND(Fact(risk_calc='low'), ProjectSpecs(q_time='time')))
    def culture_reliable(self):
        self.declare(Fact(culture='reliable'))
        self._log("Культура: Надежно (Есть время и ресурсы для корпоративной архитектуры)")

    # ==========================================
    # УРОВЕНЬ 4: СТОЛПЫ (СПОСОБ ЗАГРУЗКИ, ДАННЫЕ, СЕРВЕРА, ДИЗАЙН, МОБИЛЬНОСТЬ)
    # ==========================================

    @Rule(AND(Fact(perf_calc='critical'), ProjectSpecs(q_seo='yes')))
    def render_ssg(self):
        self.declare(Fact(render='SSG'))

    @Rule(AND(Fact(perf_calc='normal'), ProjectSpecs(q_seo='yes')))
    def render_ssr(self):
        self.declare(Fact(render='SSR'))

    @Rule(ProjectSpecs(q_seo='no'))
    def render_spa(self):
        self.declare(Fact(render='SPA'))

    @Rule(OR(ProjectSpecs(q_real='yes'), ProjectSpecs(q_offline='yes')))
    def state_complex(self):
        self.declare(Fact(state='Complex'))

    @Rule(AND(ProjectSpecs(q_real='no'), ProjectSpecs(q_offline='no')))
    def state_simple(self):
        self.declare(Fact(state='Simple'))

    @Rule(AND(ProjectSpecs(q_host='little'), ProjectSpecs(q_traffic='yes')))
    def infra_cloud(self):
        self.declare(Fact(infra='Cloud'))

    @Rule(OR(ProjectSpecs(q_host='much'), ProjectSpecs(q_traffic='no')))
    def infra_own(self):
        self.declare(Fact(infra='Own'))

    @Rule(AND(ProjectSpecs(q_lib='yes'), ProjectSpecs(q_anim='no')))
    def ui_kit(self):
        self.declare(Fact(ui='UI-Kit'))

    @Rule(OR(ProjectSpecs(q_lib='no'), ProjectSpecs(q_anim='yes')))
    def ui_custom(self):
        self.declare(Fact(ui='Custom'))

    @Rule(ProjectSpecs(q_store='no'))
    def mobile_web(self):
        self.declare(Fact(mobile='Web'))

    @Rule(AND(ProjectSpecs(q_store='yes'), ProjectSpecs(native_req='no')))
    def mobile_pwa(self):
        self.declare(Fact(mobile='PWA'))

    @Rule(AND(ProjectSpecs(q_store='yes'), ProjectSpecs(native_req='yes')))
    def mobile_native(self):
        self.declare(Fact(mobile='Native'))

    # ==========================================
    # УРОВЕНЬ 5: ИТОГОВЫЙ ВЫБОР
    # ==========================================

    @Rule(Fact(mobile='Native'))
    def rec_react_native(self):
        reason = (
            "Вы выбрали публикацию в AppStore/GooglePlay и указали, что "
            "требуется доступ к функциям мобильного телефона (например, камере, геопозиции или контактам). "
            "Для таких задач нативная кроссплатформенная разработка с использованием **React Native** (или Flutter) "
            "является наиболее подходящим решением. Это обеспечит и веб-версию (через React), и полноценные мобильные приложения."
        )
        self._print_result("React Native", reason)

    @Rule(AND(Fact(culture='reliable'), Fact(render='SPA')))
    def rec_angular_spa(self):
        reason = (
            "**Angular (SPA)**\n"
            "Поскольку SEO не требуется, но нужна надежная Enterprise-разработка с долговременной поддержкой "
            "и сложной работой с данными, Angular (SPA) будет отличным вариантом для создания масштабируемых внутренних порталов или CRM."
        )
        self._print_result("Angular (SPA)", reason)

    @Rule(AND(Fact(culture='fast'), Fact(render='SPA')))
    def rec_vue_spa(self):
        reason = (
            "**Vue.js / React (SPA)**\n"
            "SEO не требуется, открывается путь к классическому Single Page Application (SPA). "
            "Благодаря выбору культуры «Быстро» (MVP, горят сроки), Vue.js или React (Vite) идеально подойдут "
            "за счет мягкой кривой обучения и огромной экосистемы."
        )
        self._print_result("Vue.js / React (SPA)", reason)

    @Rule(AND(Fact(culture='reliable'), OR(Fact(render='SSG'), Fact(render='SSR'))))
    def rec_angular_seo(self):
        reason = (
            "**Angular (SEO/SSG)**\n"
            "Выбираем, если это Enterprise-портал (например, банковский сайт или кабинет госуслуг). "
            "Да, там нужен SEO, но важнее — строгая типизация, архитектура «из коробки» и долгосрочная поддержка (Long Term Support).\n\n"
            "*Критерий: Строгая архитектура + SEO.*"
        )
        self._print_result("Angular", reason)

    @Rule(AND(Fact(team_cap='strong'), OR(Fact(render='SSG'), Fact(render='SSR'))))
    def rec_next(self):
        reason = (
            "**Next.js (SEO/SSG)**\n"
            "Это «золотой стандарт» для E-commerce и Маркетинга. Лучшая интеграция с облаками (Vercel) "
            "и огромный выбор готовых библиотек.\n\n"
            "*Критерий: Гибкая архитектура + Максимальный SEO + Популярный стек.*"
        )
        self._print_result("Next.js", reason)

    @Rule(AND(Fact(culture='fast'), Fact(team_cap='weak'), OR(Fact(render='SSG'), Fact(render='SSR'))))
    def rec_nuxt(self):
        reason = (
            "**Nuxt (SEO/SSG)**\n"
            "Выбираем для быстрых контентных проектов и среднего бизнеса. У Nuxt лучший Developer Experience (DX) "
            "— всё настраивается автоматически.\n\n"
            "*Критерий: Скорость разработки + SEO + Малая команда.*"
        )
        self._print_result("Nuxt", reason)

    @Rule(Fact(render='SSG'))
    def rec_astro(self):
        reason = (
            "**Astro (SSG)**\n"
            "Выбираем, когда Производительность выше всего. Он выдает «Zero JS» на клиенте. "
            "Если это лендинг или статический каталог, где каждая миллисекунда — это деньги, Astro побеждает всех.\n\n"
            "*Критерий: Контентный сайт + Критическая скорость.*"
        )
        self._print_result("Astro", reason)

    def _print_result(self, stack, reason):
        self.recommendations.append({"stack": stack, "reason": reason})
        print(f"\n[ РЕЗУЛЬТАТ ] {stack}")
