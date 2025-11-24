/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

import {
  PrefixSuffixFormatter,
  createD3NumberFormatter,
} from '@superset-ui/core';

it('PrefixSuffixFormatter without prefix and suffix', () => {
  const prefixSuffixFormatter = new PrefixSuffixFormatter({
    formatter: createD3NumberFormatter({ formatString: '.2f' }),
  });
  expect(prefixSuffixFormatter.format(1000)).toBe('1000.00');
  expect(prefixSuffixFormatter(1000)).toBe('1000.00');
});

it('PrefixSuffixFormatter with prefix', () => {
  const prefixSuffixFormatter = new PrefixSuffixFormatter({
    formatter: createD3NumberFormatter({ formatString: '.2f' }),
    prefix: 'PRE-',
  });
  expect(prefixSuffixFormatter.format(1000)).toBe('PRE-1000.00');
  expect(prefixSuffixFormatter(1000)).toBe('PRE-1000.00');
});

it('PrefixSuffixFormatter suffix', () => {
  const prefixSuffixFormatter = new PrefixSuffixFormatter({
    formatter: createD3NumberFormatter({ formatString: '.2f' }),
    suffix: '-SUF',
  });
  expect(prefixSuffixFormatter.format(1000)).toBe('1000.00-SUF');
  expect(prefixSuffixFormatter(1000)).toBe('1000.00-SUF');
});

it('PrefixSuffixFormatter with prefix and suffix', () => {
  const prefixSuffixFormatter = new PrefixSuffixFormatter({
    formatter: createD3NumberFormatter({ formatString: '.2f' }),
    prefix: 'PRE-',
    suffix: '-SUF',
  });
  expect(prefixSuffixFormatter.format(1000)).toBe('PRE-1000.00-SUF');
  expect(prefixSuffixFormatter(1000)).toBe('PRE-1000.00-SUF');
});
