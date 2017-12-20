/* LanguageTool, a natural language style checker
 * Copyright (C) 2017 Daniel Naber (http://www.danielnaber.de)
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
 * USA
 */
package org.languagetool.language;

import org.languagetool.Language;
<<<<<<< HEAD:languagetool-language-modules/sr/src/test/java/org/languagetool/language/SerbianConcurrencyTest.java
import org.languagetool.language.AbstractLanguageConcurrencyTest;
import org.languagetool.language.Serbian;
=======
>>>>>>> e8f4ad8238abfb79fe729c777f07d0ad8a9caf25:languagetool-language-modules/sr/src/test/java/org/languagetool/language/SerbianConcurrencyTest.java

/**
 * Test class
 *
 * @author Zoltán Csala
<<<<<<< HEAD:languagetool-language-modules/sr/src/test/java/org/languagetool/language/SerbianConcurrencyTest.java
 *
 * @since 4.0
=======
>>>>>>> e8f4ad8238abfb79fe729c777f07d0ad8a9caf25:languagetool-language-modules/sr/src/test/java/org/languagetool/language/SerbianConcurrencyTest.java
 */
public class SerbianConcurrencyTest extends AbstractLanguageConcurrencyTest {

  @Override
  protected Language createLanguage() {
    return new Serbian();
  }

  @Override
  protected String createSampleText() {
    return "Материјал из Википедије, слободне енклицопедије.";
  }
}
