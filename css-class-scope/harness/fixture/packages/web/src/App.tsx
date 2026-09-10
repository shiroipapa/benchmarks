import React from 'react';

export function PricingPage() {
  return (
    <section className="hero hero--dark">
      <h1 className="hero__title">Ship faster with Acme</h1>
      <div className="hero__actions">
        <a className="ds-button ds-button--primary" href="/signup">
          <span className="ds-button__label">Start free</span>
        </a>
      </div>
      <div className="ds-grid ds-grid--3">
        <article className="pricing-card pricing-card--featured">
          <div className="pricing-card__price">$29</div>
        </article>
      </div>
    </section>
  );
}
