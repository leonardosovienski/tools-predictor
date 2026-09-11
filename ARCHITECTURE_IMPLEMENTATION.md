# Implementação arquitetural — 2026-09-11

Release 4.2.0 publicada; não constitui autorização de execução econômica.

- Schema 3 permite jobs genéricos sem identidade econômica. Schemas 1 e 2 continuam legíveis; v2 mantém seus requisitos.
- A identidade econômica recusa U+001F, preservando os bytes e hashes das identidades válidas existentes.
- EXECUTION exige chave econômica, todos os campos de risco explicitamente informados, cinco limites finitos, `risk_source`, `risk_max_age_seconds`, `source` coincidente e `observed_at` com fuso. Ausência, snapshot futuro ou vencido bloqueia o subprocesso. Nenhum default concede segurança por omissão.
- Um lock do sistema operacional serializa verificação de propriedade, renovação, substituição e remoção da lease local. O arquivo `.mutation.guard` permanece no diretório; não removê-lo durante uso.

Migração: parar os runners antigos antes de usar 4.2 no mesmo runtime root. Não misturar versões de protocolo de lock. Usar inicialmente uma raiz nova e fixtures. Não alterar ledgers antigos nem recalcular chaves válidas. Rollback do pacote exige parar runners e avaliar operações pendentes; não apagar registros de reconciliação.

Validação final: suíte de 76 testes passou com cobertura 87,90%, incluindo takeover concorrente de lease vencida. Ruff e Pyright aprovados; oito testes de risco foram repetidos após a correção de tipagem das fixtures. Windows local não substitui a matriz Linux/Windows da CI. Os controles não autenticam a origem do risco nem provam segurança econômica: `risk_source` é uma identidade configurada pelo operador.

A matriz remota Linux/Windows passou, além da release. O upload do SBOM no workflow foi corrigido para manter artefato de CI sem exigir escrita em releases; a CI do main 4b641909 passou após a correção.

## Entrega arquitetural publicada — 11/09/2026

Versão **4.2.0** publicada: [release e artefatos](https://github.com/leonardosovienski/predictor-ops/releases/tag/v4.2.0). [CI de engenharia aprovada](https://github.com/leonardosovienski/predictor-ops/actions/runs/34628184138) para a fonte `e804ac8b5173156737e2212d9bd47cd3f2072700`. Consulte [ARCHITECTURE_IMPLEMENTATION.md](ARCHITECTURE_IMPLEMENTATION.md) para comportamento, migração e limites. Este registro atualiza a entrega de software; estados científicos e registros datados abaixo conservam sua autoridade e contexto histórico.
