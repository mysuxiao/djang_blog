var customSearch;
!(function (t) {
  "use strict";
  const o = 70;
  function a(e, a) {
    a = a || o;
    const n = e.href ? t(e.getAttribute("href")) : t(e);
    t("html, body").animate({ scrollTop: n.offset().top - a }, 400);
  }
  t(function () {
    var n;
    !(function () {
      if (!window.subData) return;
      const e = t("header .wrapper"),
        o = t(".s-comment", e),
        n = t(".s-toc", e);
      e.find(".nav-sub .logo").text(window.subData.title);
      let c = document.body.scrollTop;
      t(document, window).scroll(() => {
        const o = t(window).scrollTop(),
          a = o - c;
        a >= 50 && o > 100
          ? ((c = o), e.addClass("sub"))
          : a <= -50 && ((c = o), e.removeClass("sub"));
      });
      const s = t("#comments");
      s.length
        ? o.click((e) => {
            e.preventDefault(), e.stopPropagation(), a(s);
          })
        : o.remove();
      const r = t(".toc-wrapper");
      r.length && r.children().length
        ? n.click((e) => {
            e.stopPropagation(), r.toggleClass("active");
          })
        : n.remove();
    })(),
      (function () {
        var e = t("header .menu");
        e.find("li a.active").removeClass("active");
        var o,
          a = location.pathname.replace(/\/|%/g, "");
        0 == a.length && (a = "home");
        var n = a.match(/page\d{0,}$/g);
        n && ((n = n[0]), (a = a.split(n)[0]));
        var c,
          s = a.match(/index.html/);
        s && ((s = s[0]), (a = a.split(s)[0])),
          (o = t("#" + a, e)),
          (c = o) &&
            c.length &&
            c.addClass("active").siblings().removeClass("active");
      })(),
      (n = t(".l_header .switcher .s-menu")).click(function (e) {
        e.stopPropagation(),
          t("body").toggleClass("z_menu-open"),
          n.toggleClass("active");
      }),
      t(document).click(function (e) {
        t("body").removeClass("z_menu-open"), n.removeClass("active");
      }),
      (function () {
        var o = t(".l_header .switcher .s-search"),
          a = t(".l_header"),
          n = t(".l_header .m_search");
        0 !== o.length &&
          (o.click(function (e) {
            e.stopPropagation(),
              a.toggleClass("z_search-open"),
              n.find("input").focus();
          }),
          t(document).click(function (e) {
            a.removeClass("z_search-open");
          }),
          n.click(function (e) {
            e.stopPropagation();
          }),
          a.ready(function () {
            a.bind("keydown", function (t) {
              if (9 == t.keyCode) return !1;
              var o,
                a,
                n = !!document.all;
              n
                ? ((o = window.event.keyCode), (a = window.event))
                : ((o = e.which), (a = e)),
                9 == o &&
                  (n
                    ? ((a.keyCode = 0), (a.returnValue = !1))
                    : ((a.which = 0), a.preventDefault()));
            });
          }));
      })(),
      (function () {
        const e = t(".toc-wrapper");
        if (0 === e.length) return;
        t(document).click(() => e.removeClass("active")),
          e.on("click", "a", (t) => {
            t.preventDefault(),
              t.stopPropagation(),
              "A" === t.target.tagName
                ? a(t.target)
                : "SPAN" === t.target.tagName && a(t.target.parentElement),
              e.removeClass("active");
          });
        const n = Array.from(e.find("li a")),
          c = () =>
            n.map((e) =>
              Math.floor(t(e.getAttribute("href")).offset().top - o),
            );
        let s = c();
        const r = () => {
          const e = t("html").scrollTop() || t("body").scrollTop();
          if (!s) return;
          let o,
            a = 0,
            c = s.length - 1;
          for (; a < c; )
            s[(o = (a + c + 1) >> 1)] === e
              ? (a = c = o)
              : s[o] < e
                ? (a = o)
                : (c = o - 1);
          t(n).removeClass("active").eq(a).addClass("active");
        };
        t(window)
          .resize(() => {
            (s = c()), r();
          })
          .scroll(() => {
            r();
          }),
          r();
      })(),
      (function () {
        const e = t(".s-top", ".l_body");
        let o = document.body.scrollTop;
        t(document, window).scroll(() => {
          const a = t(window).scrollTop(),
            n = a - o;
          a > 150
            ? ((o = a),
              e.addClass("show"),
              n > 0 ? e.removeClass("hl") : e.addClass("hl"))
            : ((o = a), e.removeClass("show").removeClass("hl"));
        }),
          e.click(() => a(document.body));
      })(),
      setTimeout(function () {
        t("#loading-bar-wrapper").fadeOut(500);
      }, 300),
      "google" === SEARCH_SERVICE
        ? (customSearch = new GoogleCustomSearch({
            apiKey: GOOGLE_CUSTOM_SEARCH_API_KEY,
            engineId: GOOGLE_CUSTOM_SEARCH_ENGINE_ID,
            imagePath: "/images/",
          }))
        : "algolia" === SEARCH_SERVICE
          ? (customSearch = new AlgoliaSearch({
              apiKey: ALGOLIA_API_KEY,
              appId: ALGOLIA_APP_ID,
              indexName: ALGOLIA_INDEX_NAME,
              imagePath: "/images/",
            }))
          : "hexo" === SEARCH_SERVICE
            ? (customSearch = new HexoSearch({ imagePath: "/images/" }))
            : "azure" === SEARCH_SERVICE
              ? (customSearch = new AzureSearch({
                  serviceName: AZURE_SERVICE_NAME,
                  indexName: AZURE_INDEX_NAME,
                  queryKey: AZURE_QUERY_KEY,
                  imagePath: "/images/",
                }))
              : "baidu" === SEARCH_SERVICE &&
                (customSearch = new BaiduSearch({
                  apiId: BAIDU_API_ID,
                  imagePath: "/images/",
                }));
  });
})(jQuery);
