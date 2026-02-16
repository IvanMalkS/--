const KNOWLAGE_TREE = {
  question: 'Какой тип проекта разрабатываем?',
  options: [
    {
      text: 'Лендинг / Контентный сайт',
      next: {
        question: 'Нужен сложный интерактив (формы, калькуляторы)?',
        options: [
          { text: 'Нет (простая визитка)', result: 'HTML/CSS + Vanilla JS' },
          { text: 'Да (Блог / Документация)', result: 'Astro' },
        ],
      },
    },
    {
      text: 'Веб-приложение (Сервис / SaaS)',
      next: {
        question: 'Масштаб и архитектура проекта?',
        options: [
          {
            text: 'Enterprise / Сложный B2B',
            next: {
              question: 'Критичен ли SEO / SSR?',
              options: [
                { text: 'Да (Публичный портал)', result: 'Angular + SSR' },
                { text: 'Нет (Закрытая CRM)', result: 'Angular SPA' },
              ],
            },
          },
          {
            text: 'Startup / SaaS / B2C',
            next: {
              question: 'Критичен ли SEO / SSR?',
              options: [
                {
                  text: 'Да (Магазин, СМИ)',
                  next: {
                    question: 'Какой стек ближе команде?',
                    options: [
                      { text: 'React экосистема', result: 'Next.js' },
                      { text: 'Vue экосистема', result: 'Nuxt' },
                    ],
                  },
                },
                {
                  text: 'Нет (SPA / Dashboard)',
                  next: {
                    question: 'Что важнее в разработке?',
                    options: [
                      { text: 'Экосистема и легкий найм', result: 'Vite + React' },
                      { text: 'Скорость разработки и DX', result: 'Vue 3 / Svelte' },
                    ],
                  },
                },
              ],
            },
          },
        ],
      },
    },
  ],
};

const copyTree = (tree) => JSON.parse(JSON.stringify(tree));

const knowledgeBase = copyTree(KNOWLAGE_TREE);

let currentNode = knowledgeBase;

function render() {
  const questionElement = document.getElementById('question');
  const optionElement = document.getElementById('options');

  optionElement.innerHTML = '';

  if (currentNode.result) {
    questionElement.innerText = 'Рекомендуемый стек:';

    const resultConteiner = document.createElement('div');
    resultConteiner.className = 'result-container';

    const resultText = document.createElement('div');
    resultText.className = 'result';
    resultText.innerText = currentNode.result;

    const resetbutton = document.createElement('button');
    resetbutton.innerText = 'Начать заново';
    resetbutton.className = 'reset-button';
    resetbutton.onclick = reset;

    resultConteiner.appendChild(resultText);
    resultConteiner.appendChild(resetbutton);
    optionElement.appendChild(resultConteiner);
    return;
  }

  questionElement.innerText = currentNode.question;

  currentNode.options.forEach((opt) => {
    const button = document.createElement('button');
    button.innerText = opt.text;
    button.onclick = () => {
      currentNode = opt.next || { result: opt.result };
      render();
    };
    optionElement.appendChild(button);
  });
}

function reset() {
  currentNode = knowledgeBase;
  render();
}

render();
