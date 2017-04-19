import { HomeProxyPage } from './app.po';

describe('home-proxy App', () => {
  let page: HomeProxyPage;

  beforeEach(() => {
    page = new HomeProxyPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
