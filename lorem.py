# -*- coding: utf-8 -*-
"""lorem ipsum generator

In publishing and graphic design, lorem ipsum is a placeholder text commonly
used to demonstrate the visual form of a document or a typeface without
relying on meaningful content.

The :mod:`lorem` module provides a generic access to generating the lorem ipsum
text from its very original text::

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
    veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
    commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit
    esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
    cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
    est laborum.

Usage of the :mod:`lorem` module is rather simple. Depending on your needs, the
:mod:`lorem` module provides generation of *words*, *sentences*, and
*paragraphs*.

Get Random Words
----------------

The :mod:`lorem` module provides two different ways for getting random words.

1. :func:`word` -- generate a list of random words

   .. code-block:: python

      word(count=1, func=None, args=(), kwargs={}) -> Iterator[str]

2. :func:`get_word` -- return random words

   .. code-block:: python

      get_word(count=1, sep=' ', func=None, args=(), kwargs={}) -> str

Get Random Sentences
--------------------

The :mod:`lorem` module provides two different ways for getting random sentences.

1. :func:`sentence` -- generate a list of random sentences

   .. code-block:: python

      sentence(count=1, comma=(0, 2), word_range=(4, 8)) -> Iterator[str]

2. :func:`get_sentence` -- return random sentences

   .. code-block:: python

      get_sentence(count=1, sep=' ', comma=(0, 2), word_range=(4, 8)) -> Union[str]

Get Random Paragraphs
---------------------

The :mod:`lorem` module provides two different ways for getting random paragraphs.

1. :func:`paragraph` -- generate a list of random paragraphs

   .. code-block:: python

      paragraph(count=1, comma=(0, 2), word_range=(4, 8), sentence_range=(5, 10)) -> Iterator[str]

2. :func:`get_paragraph` -- return random paragraphs

   .. code-block:: python

      get_paragraph(count=1, sep=os.linesep, comma=(0, 2), word_range=(4, 8), sentence_range=(5, 10)) -> Union[str]

Customise Word Pool
-------------------

If wanted, the :mod:`lorem` module also provides an interface to customise the word
pool as you wish.

1. :func:`set_pool` -- customise random word pool

   .. code-block:: python

      set_pool(pool)

"""
import itertools
import os
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable, Iterable, Iterator, Optional

__all__ = [
    'set_pool',
    'word', 'sentence', 'paragraph',
    'get_word', 'get_sentence', 'get_paragraph',
]

#: The original lorem ipsum text pool.
_TEXT = ('ad', 'adipiscing', 'aliqua', 'aliquip', 'amet', 'anim', 'aute', 'cillum', 'commodo',
         'consectetur', 'consequat', 'culpa', 'cupidatat', 'deserunt', 'do', 'dolor', 'dolore',
         'duis', 'ea', 'eiusmod', 'elit', 'enim', 'esse', 'est', 'et', 'eu', 'ex', 'excepteur',
         'exercitation', 'fugiat', 'id', 'in', 'incididunt', 'ipsum', 'irure', 'labore', 'laboris',
         'laborum', 'lorem', 'magna', 'minim', 'mollit', 'nisi', 'non', 'nostrud', 'nulla',
         'occaecat', 'officia', 'pariatur', 'proident', 'qui', 'quis', 'reprehenderit', 'sed',
         'sint', 'sit', 'sunt', 'tempor', 'ullamco', 'ut', 'velit', 'veniam', 'voluptate')


def _gen_pool(dupe: 'int' = 1) -> 'Iterator[str]':
    """Generate word pool.

    Args:
        dupe: Duplication to generate the word pool.

    Returns:
        An infinite loop word pool.

    """
    pool = []  # type: list[str]
    for _ in range(dupe):
        pool.extend(_TEXT)
    random.shuffle(pool)

    while pool:  # pragma: no cover
        for text in pool:
            yield text
        random.shuffle(pool)


def _gen_word(pool: 'Iterator[str]',  # pylint: disable=dangerous-default-value
              func: 'Optional[str | Callable[[str], str]]' = None,
              args: 'tuple[str, ...]' = (), kwargs: 'dict[str, Any]' = {}) -> 'str':
    """Generate random word.

    Args:
        pool: Word pool, returned by :func:`_gen_pool`.
        func: Filter function. It can be an attribute name of :obj:`str`, or a customised
            function that takes the original :obj:`str` and returns the modified :obj:`str`.
        args:  Additional positional arguments for ``func``.
        kwargs: Additional keyword arguments for ``func``.

    Returns:
        Random word.

    """
    text = next(pool)
    if func is not None:
        if isinstance(func, str):
            text = getattr(text, func)(*args, **kwargs)
        else:
            text = func(text, *args, **kwargs)
    return text


def _gen_sentence(pool: 'Iterator[str]',
                  comma: 'tuple[int, int]',
                  word_range: 'tuple[int, int]') -> 'str':
    """Generate random sentence.

    Args:
        pool: Word pool, returned by :func:`_gen_pool`.
        comma: Random range for number of commas. The function will use :func:`random.randint`
            to choose a random integer as the number of commas.
        word_range: Random range for number of words in each sentence. The function will use
            :func:`random.randint` to choose a random integer as the number of words.

    Returns:
        Random sentence.

    """
    text = _gen_word(pool=pool, func='capitalize')
    for _ in range(random.randint(*word_range) - 1):  # nosec B311
        text += ' ' + _gen_word(pool=pool)

    for _ in range(random.randint(*comma)):  # nosec B311
        include_comma = random.choice([True, False])  # nosec B311
        if include_comma:
            text += ','
            for _ in range(random.randint(*word_range)):  # nosec B311
                text += ' ' + _gen_word(pool=pool)
            continue
        break
    return text + '.'


def _gen_paragraph(pool: 'Iterator[str]',
                   comma: 'tuple[int, int]',
                   word_range: 'tuple[int, int]',
                   sentence_range: 'tuple[int, int]') -> 'str':
    """Generate random paragraph.

    Args:
        pool: Word pool, returned by :func:`_gen_pool`.
        comma: Random range for number of commas. The function will use :func:`random.randint`
            to choose a random integer as the number of commas.
        word_range: Random range for number of words in each sentence. The function will use
            :func:`random.randint` to choose a random integer as the number of words.
        sentence_range: Random range for number of sentences in each  paragraph. The function
            will use :func:`random.randint` to choose a random integer as the number of sentences.

    Returns:
        Random paragraph.

    """
    text = _gen_sentence(pool=pool, comma=comma, word_range=word_range)
    for _ in range(random.randint(*sentence_range) - 1):  # nosec B311
        text += ' ' + _gen_sentence(pool=pool, comma=comma, word_range=word_range)
    return text


def word(count: int = 1,  # pylint: disable=dangerous-default-value
         func: 'Optional[str | Callable[[str], str]]' = None,
         args: 'tuple[str, ...]' = (), kwargs: 'dict[str, Any]' = {}) -> 'Iterator[str]':
    """Generate a list of random words.

    .. code-block:: python

        >>> list(itertools.cycle(word(count=3), 3))
        ['labore', 'tempor', 'commodo']
        >>> list(itertools.cycle(word(count=3, func='capitalize'), 3))
        ['Ea', 'Lorem', 'Do']
        >>> list(itertools.cycle(word(count=3, func=lambda s: s.upper()), 3))
        ['UT', 'AMET', 'EXCEPTEUR']

    Args:
        count: Number of non-repeated random words.
        func: Filter function. It can be an attribute name of :obj:`str`, or a customised
            function that takes the original :obj:`str` and returns the modified :obj:`str`.
        args: Additional positional arguments for ``func``.
        kwargs: Additional keyword arguments for ``func``.

    Returns:
        Indefinite random words generator.

    """
    pool = _gen_pool(count)
    yield from itertools.cycle(_gen_word(pool=pool,
                                         func=func,
                                         args=args,
                                         kwargs=kwargs) for _ in range(count))


def sentence(count: 'int' = 1,
             comma: 'tuple[int, int]' = (0, 2),
             word_range: 'tuple[int, int]' = (4, 8)) -> 'Iterator[str]':
    """Generate a list of random sentences.

    .. code-block:: python

        >>> list(itertools.islice(sentence(), 1))
        ['Aute irure et commodo sunt do duis dolor.']

    Args:
        count: Number of non-repeated random sentences.
        comma: Random range for number of commas. The function will use :func:`random.randint`
            to choose a random integer as the number of commas.
        word_range: Random range for number of words in each sentence. The function will use
            :func:`random.randint` to choose a random integer as the number of words.

    Returns:
        Indefinite random sentence generator.

    """
    pool = _gen_pool(count * random.randint(*word_range))  # nosec B311
    yield from itertools.cycle(_gen_sentence(pool=pool,
                                             comma=comma,
                                             word_range=word_range) for _ in range(count))


def paragraph(count: 'int' = 1,
              comma: 'tuple[int, int]' = (0, 2),
              word_range: 'tuple[int, int]' = (4, 8),
              sentence_range: 'tuple[int, int]' = (5, 10)) -> 'Iterator[str]':
    """Generate a list of random paragraphs.

    .. code-block:: python

        >>> list(itertools.islice(paragraph(), 1))
        ['Aute sint et cupidatat aliquip. Non exercitation est aliquip voluptate '
         'fugiat, reprehenderit ad occaecat laboris velit consequat. Magna enim '
         'deserunt aute laborum fugiat exercitation. Aliqua ex sunt fugiat in '
         'magna voluptate. Elit nisi exercitation nostrud. Magna proident et '
         'fugiat eiusmod cupidatat fugiat, sit culpa fugiat non ea eu '
         'reprehenderit elit. Proident mollit mollit ut cillum. Nostrud voluptate '
         'aliquip cupidatat anim.']

    Args:
        count: Number of non-repeated random paragraphs.
        comma: Random range for number of commas. The function will use :func:`random.randint`
            to choose a random integer as the number of commas.
        word_range: Random range for number of words in each sentence. The function will use
            :func:`random.randint` to choose a random integer as the number of words.
        sentence_range: Random range for number of sentences in each paragraph. The function
            will use :func:`random.randint` to choose a random integer as the number of sentences.

    Returns:
        Random paragraph generator.

    """
    pool = _gen_pool(count * random.randint(*word_range) * random.randint(*sentence_range))  # nosec B311
    yield from itertools.cycle(_gen_paragraph(pool=pool,
                                              comma=comma,
                                              word_range=word_range,
                                              sentence_range=sentence_range) for _ in range(count))


def get_word(count: 'int | tuple[int, int]' = 1,  # pylint: disable=dangerous-default-value
             sep: 'str' = ' ',
             func: 'Optional[str | Callable[[str], str]]' = None,
             args: 'tuple[str, ...]' = (), kwargs: 'dict[str, Any]' = {}) -> 'str':
    """Return random words.

    .. code-block:: python

        >>> get_word(count=3)
        'anim voluptate non'
        >>> get_word(count=3, func='capitalize')
        'Non Labore Ut'
        >>> get_word(count=3, func=lambda s: s.upper())
        'NISI TEMPOR CILLUM'

    Args:
        count: Number of random words. To generate random number of words, supply a 2-element
            tuple of :obj:`int`, the function will use :func:`random.randint` to choose a
            random integer as the number of random words.
        sep: Seperator between each word.
        func: Filter function. It can be a function name of :obj:`str`, or a customised
            function that takes the original :obj:`str` and returns the modified :obj:`str`.
        args: Additional positional arguments for ``func``.
        kwargs: Additional keyword arguments for ``func``.

    Returns:
        :obj:`str`: Random words.

    """
    if isinstance(count, tuple):
        count = random.randint(*count)  # nosec B311
    return sep.join(itertools.islice(word(count, func, args, kwargs), count))


def get_sentence(count: 'int | tuple[int, int]' = 1,
                 sep: 'str' = ' ',
                 comma: 'tuple[int, int]' = (0, 2),
                 word_range: 'tuple[int, int]' = (4, 8)) -> 'str':
    """Return random sentences.

    .. code-block:: python

        >>> get_sentence()
        'Nostrud laboris lorem minim sit culpa, aliqua nostrud in amet, sint pariatur eiusmod esse.'

    Args:

        count: Number of random sentences. To generate random number of sentences, supply a
            2-element tuple of :obj:`int`, the function will use :func:`random.randint` to
            choose a random integer as the number of random sentences.
        sep: Seperator between each sentence.
        comma: Random range for number of commas. The function will use :func:`random.randint`
            to choose a random integer as the number of commas.
        word_range: Random range for number of words in each sentence. The function will use
            :func:`random.randint` to choose a random integer as the number of words.

    Returns:
        Random sentences.

    """
    if isinstance(count, tuple):
        count = random.randint(*count)  # nosec B311
    return sep.join(itertools.islice(sentence(count, comma, word_range), count))


def get_paragraph(count: 'int | tuple[int, int]' = 1,
                  sep: 'str' = os.linesep,
                  comma: 'tuple[int, int]' = (0, 2),
                  word_range: 'tuple[int, int]' = (4, 8),
                  sentence_range: 'tuple[int, int]' = (5, 10)) -> 'str':
    r"""Return random paragraphs.

    .. code-block:: python

        >>> get_paragraph()
        'Exercitation magna sunt excepteur irure adipiscing commodo duis. Est '
        'ipsum qui deserunt, deserunt nostrud reprehenderit esse. Do velit '
        'est in velit sed. Sunt officia officia lorem. Commodo lorem '
        'exercitation veniam officia pariatur velit. Deserunt deserunt sed '
        'consequat laborum consequat dolor. Et consectetur irure sint elit tempor,'
        ' est minim nisi eiusmod id excepteur. Minim cillum veniam sed aliquip '
        'anim sit, pariatur nostrud ex cillum laboris laborum. Laborum ullamco '
        'mollit elit. Amet id incididunt ipsum sed.'

    Args:
        count: Number of random paragraphs. To generate random number of paragraphs, supply a
            2-element tuple of :obj:`int`, the function will use :func:`random.randint` to choose
            a random integer as the number of random paragraphs.
        sep: Seperator between each paragraph. The default value is OS-dependent as :data:`os.linsep`
            (``\r\n`` on Windows, ``\n`` on POSIX).
        comma: Random range for number of commas. The function will use :func:`random.randint` to choose
            a random integer as the number of commas.
        word_range: Random range for number of words in each sentence. The function will use
            :func:`random.randint` to choose a random integer as the number of words.
        sentence_range: Random range for number of sentences in each paragraph. The function will use
            :func:`random.randint` to choose a random integer as the number of sentences.

    Returns:
        Random paragraphs.

    """
    if isinstance(count, tuple):
        count = random.randint(*count)  # nosec B311
    return sep.join(itertools.islice(paragraph(count, comma, word_range, sentence_range), count))


def set_pool(pool: 'Iterable[str]') -> 'None':
    """Customise random word pool.

    Args:
        pool: List of words to be used as random word pool.

    """
    global _TEXT  # pylint: disable=global-statement
    _TEXT = pool  # type: ignore[assignment]
